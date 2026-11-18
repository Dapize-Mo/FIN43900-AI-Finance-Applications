"""Deadline-aware transient retry tests — Oladapo Olaniyan, FIN-43900.
Reproduces the Oct 16-Nov 5 Modal failures (503 high demand, request timeouts)
that left 32 delivered events without a submitted prediction."""
from types import SimpleNamespace
import pytest
import predict


class APITimeoutError(Exception):  # same class name the OpenAI SDK raises
    pass


def _ok(v):
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(parsed=predict.Prediction(predicted_percentile=v)))])


def _err(code):
    e = RuntimeError(f"status {code}"); e.status_code = code; return e


class FakeClock:
    def __init__(self): self.t = 1000.0
    def now(self): return self.t
    def sleep(self, s): self.t += s


def _install(monkeypatch, outcomes, per_call_seconds=1.0):
    calls = []; clock = FakeClock()
    def parse(**kw):
        calls.append(kw["model"]); clock.t += per_call_seconds
        o = outcomes.pop(0) if outcomes else _err(503)
        if isinstance(o, Exception): raise o
        return _ok(o)
    monkeypatch.setenv("GEMINI_API_KEY", "fake")
    monkeypatch.setattr(predict, "_openai", SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(parse=parse))))
    monkeypatch.setattr(predict, "_clock", clock.now)
    monkeypatch.setattr(predict, "_sleep", clock.sleep)
    return calls, clock


def test_timeout_on_primary_uses_fallback(monkeypatch):
    calls, _ = _install(monkeypatch, [APITimeoutError("Request timed out."), 0.41])
    assert predict._ask_current(summary={}, ticker="TRST", event_type="EARNINGS_RELEASE", seconds_left=290) == 0.41
    assert calls == ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]


def test_both_models_503_then_recovers_with_backoff(monkeypatch):
    calls, _ = _install(monkeypatch, [_err(503), _err(503), _err(503), 0.66])
    assert predict._ask_current(summary={}, ticker="CRAI", event_type="EARNINGS_RELEASE", seconds_left=290) == 0.66
    assert calls == ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]


def test_rate_limit_is_transient(monkeypatch):
    calls, _ = _install(monkeypatch, [_err(429), 0.52])
    assert predict._ask_current(summary={}, ticker="X", event_type="EARNINGS_RELEASE", seconds_left=290) == 0.52


def test_persistent_outage_stops_before_deadline(monkeypatch):
    calls, clock = _install(monkeypatch, [], per_call_seconds=20.0)
    start = clock.t
    with pytest.raises(RuntimeError, match="503"):
        predict._ask_current(summary={}, ticker="X", event_type="EARNINGS_RELEASE", seconds_left=290)
    assert clock.t - start <= 290 - predict.SAFETY_SECONDS + 1e-9
    assert len(calls) >= 4


def test_no_time_left_makes_no_call(monkeypatch):
    calls, _ = _install(monkeypatch, [0.5])
    with pytest.raises(RuntimeError, match="deadline"):
        predict._ask_current(summary={}, ticker="X", event_type="EARNINGS_RELEASE", seconds_left=predict.SAFETY_SECONDS + 1)
    assert calls == []


def test_non_transient_error_is_not_retried(monkeypatch):
    calls, _ = _install(monkeypatch, [_err(400)])
    with pytest.raises(RuntimeError, match="400"):
        predict._ask_current(summary={}, ticker="X", event_type="EARNINGS_RELEASE", seconds_left=290)
    assert len(calls) == 1


def test_predict_passes_event_deadline(monkeypatch):
    seen = {}
    monkeypatch.setenv("EM_STRATEGY", "original")
    monkeypatch.setattr(predict.httpx, "get", lambda *a, **k: SimpleNamespace(raise_for_status=lambda: None, json=lambda: {"items": []}))
    def fake(**kw): seen.update(kw); return 0.5
    monkeypatch.setattr(predict, "_ask_current", fake)
    ev = {"event_type": "EARNINGS_RELEASE", "information_url": "u", "prediction_deadline": "2099-01-01T00:00:00Z",
          "focal_assets": [{"identifier_type": "TICKER", "identifier_value": "X"}]}
    assert predict.predict(ev) == [{"identifier_value": "X", "predicted_percentile": 0.5}]
    assert seen["seconds_left"] > 1000
