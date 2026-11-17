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


if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_"):
            f(); print("PASS", n)
    print("All tests passed")
