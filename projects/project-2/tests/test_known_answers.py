"""Known-answer tests. Run from project-2/:  python tests/test_known_answers.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import engine as e
from src.mandate import validate_correlation, BASE_CORRELATION

S = e.SLEEVES
COV = e.build_covariance(S, BASE_CORRELATION)


def test_01_correlation_valid():
    assert validate_correlation(BASE_CORRELATION)
    bad = [row[:] for row in BASE_CORRELATION]
    bad[0][1] = 0.5
    try:
        validate_correlation(bad)
    except ValueError:
        return
    raise AssertionError("asymmetric matrix was accepted")


def test_02_equal_weight():
    w = e.get_equal_weights()
    assert abs(e.compute_expected_return(w, S) - 0.0520) < 5e-5
    assert abs(e.compute_portfolio_volatility(w, COV) - 0.0521) < 5e-5


def test_03_benchmark():
    w = e.get_benchmark_weights()
    assert abs(e.compute_expected_return(w, S) - 0.0680) < 5e-5
    assert abs(e.compute_portfolio_volatility(w, COV) - 0.1046) < 5e-5
    assert w[0] + w[1] == 0  # zero sovereign reserve -> covenant breach


def test_04_optimizer():
    o = e.optimize_constrained_mix(S, COV)
    assert o["weights"] == [0.0, 0.08, 0.40, 0.52]
    assert o["mandate_verdict"] == "PASS"
    assert abs(o["net_return"] - 0.065) < 1e-3
    assert abs(o["volatility"] - 0.0930) < 5e-5


def test_05_kill_rule():
    s = e.run_stress_test(S, BASE_CORRELATION, equity_return_haircut_bps=100)
    assert s["is_killed"]
    assert abs(s["result"]["volatility"] - 0.1270) < 5e-5
    assert not e.run_stress_test(S, BASE_CORRELATION)["is_killed"]


def test_06_mandate_consistency():
    """Optimal portfolio passes S1-S10 checker; benchmark and equal weight fail on reserve."""
    opt = e.optimize_constrained_mix(S, COV)
    assert opt["mandate_verdict"] == "PASS"
    bench = e.evaluate_portfolio("Benchmark", e.get_benchmark_weights(), S, COV)
    eq = e.evaluate_portfolio("Equal", e.get_equal_weights(), S, COV)
    assert bench["mandate_verdict"] != "PASS" and eq["mandate_verdict"] != "PASS"
    res = sum(w for w, sl in zip(opt["weights"], S) if sl.get("reserve_eligible"))
    assert res >= 0.03 - 1e-9


def test_07_flip_test():
    """Flip test: a smaller shock must NOT kill the process; the -100 bps shock must."""
    assert not e.run_stress_test(S, BASE_CORRELATION, equity_return_haircut_bps=0)["is_killed"]
    assert e.run_stress_test(S, BASE_CORRELATION, equity_return_haircut_bps=100)["is_killed"]
    v50 = e.run_stress_test(S, BASE_CORRELATION, equity_return_haircut_bps=50)
    assert v50["is_killed"] or v50["result"]["volatility"] < 0.12


def test_08_doc_engine_concordance():
    """Memo / LCIR numbers must match what the engine produces."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    memo = open(os.path.join(root, "docs", "decision-memo.md"), encoding="utf-8").read()
    lcir = open(os.path.join(root, "docs", "validation-and-ai-use.md"), encoding="utf-8").read()
    opt = e.optimize_constrained_mix(S, COV)
    assert f"{opt['volatility']*100:.2f}%" in memo
    s = e.run_stress_test(S, BASE_CORRELATION, equity_return_haircut_bps=100)
    assert f"{s['result']['volatility']*100:.2f}%" in lcir
    assert "12.00%" in lcir and "12.00%" in memo


if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_"):
            f(); print("PASS", n)
    print("All tests passed")
