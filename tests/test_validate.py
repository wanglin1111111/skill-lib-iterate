"""skill-lib-iterate validate.py 的变异测试。

每个用例只改一个字段，断言预期维度变红。已知缺口用 strict xfail 标注：
测试当前失败（xpass 时说明缺口被修了，需要移除 marker）。
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate.py"
GOOD = ROOT / "tests" / "sample_good.json"
BAD = ROOT / "tests" / "sample_bad.json"


def load_good():
    return json.loads(GOOD.read_text(encoding="utf-8"))


def run_validator(path):
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def assert_rc(plan, expected, tmp_path, dimension=None):
    path = tmp_path / "plan.json"
    path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    result = run_validator(path)
    output = (result.stdout or "") + (result.stderr or "")
    assert result.returncode == expected, output
    if dimension:
        assert f"[{dimension}] FAIL" in result.stdout, output
    return result


def test_sample_good_passes():
    result = run_validator(GOOD)
    assert result.returncode == 0, result.stdout + result.stderr


def test_sample_bad_fails():
    result = run_validator(BAD)
    assert result.returncode == 1, result.stdout + result.stderr


# D1 事实核对
def test_star_trajectory_needs_three_anchors(tmp_path):
    plan = load_good()
    plan["fact_check"]["star_trajectory"] = plan["fact_check"]["star_trajectory"][:2]
    assert_rc(plan, 1, tmp_path, "D1")


def test_star_trajectory_must_be_numeric(tmp_path):
    plan = load_good()
    plan["fact_check"]["star_trajectory"][0]["stars_k"] = "many"
    assert_rc(plan, 1, tmp_path, "D1")


def test_star_trajectory_needs_time_anchor(tmp_path):
    plan = load_good()
    plan["fact_check"]["star_trajectory"][0]["t"] = ""
    assert_rc(plan, 1, tmp_path, "D1")


def test_actual_scale_cannot_be_below_advertised(tmp_path):
    plan = load_good()
    plan["fact_check"]["actual_scale"] = 3
    plan["fact_check"]["advertised_scale"] = 4
    assert_rc(plan, 1, tmp_path, "D1")


def test_scenario_related_cannot_be_empty(tmp_path):
    plan = load_good()
    plan["fact_check"]["scenario_related"] = []
    assert_rc(plan, 1, tmp_path, "D1")


def test_simulation_guardrail_must_be_quoted(tmp_path):
    plan = load_good()
    plan["fact_check"]["simulation_guardrail_quoted"] = False
    assert_rc(plan, 1, tmp_path, "D1")


def test_eval_limits_must_be_mapped(tmp_path):
    plan = load_good()
    plan["fact_check"]["eval_limits_mapped"] = False
    assert_rc(plan, 1, tmp_path, "D1")


@pytest.mark.xfail(
    strict=True,
    reason="已知缺口：D1 只查锚点数量/数值，没有实现文档承诺的 Star 轨迹非递减检查",
)
def test_declining_star_trajectory_should_fail(tmp_path):
    plan = load_good()
    plan["fact_check"]["star_trajectory"] = [
        {"t": "2026-07", "stars_k": 47.1},
        {"t": "2026-08", "stars_k": 39.4},
        {"t": "2026-09", "stars_k": 32.9},
    ]
    assert_rc(plan, 1, tmp_path, "D1")


# D2 底座
def test_positioning_cannot_be_empty(tmp_path):
    plan = load_good()
    plan["foundation"]["positioning"] = ""
    assert_rc(plan, 1, tmp_path, "D2")


def test_alternatives_cannot_be_empty(tmp_path):
    plan = load_good()
    plan["foundation"]["alternatives"] = []
    assert_rc(plan, 1, tmp_path, "D2")


def test_alternatives_must_include_do_nothing(tmp_path):
    plan = load_good()
    plan["foundation"]["alternatives"] = ["竞品A", "竞品B"]
    assert_rc(plan, 1, tmp_path, "D2")


def test_pending_fields_must_be_zero(tmp_path):
    plan = load_good()
    plan["foundation"]["pending_fields"] = 1
    assert_rc(plan, 1, tmp_path, "D2")


def test_replacement_test_must_pass(tmp_path):
    plan = load_good()
    plan["foundation"]["replacement_test_passed"] = False
    assert_rc(plan, 1, tmp_path, "D2")


# D3 首跑顺序
def test_audit_skill_must_run_first(tmp_path):
    plan = load_good()
    plan["first_run"]["audit_skill_first"] = False
    assert_rc(plan, 1, tmp_path, "D3")


def test_audit_needs_three_actionable_items(tmp_path):
    plan = load_good()
    plan["first_run"]["audit_actionable_items"] = 2
    assert_rc(plan, 1, tmp_path, "D3")


def test_one_action_must_land(tmp_path):
    plan = load_good()
    plan["first_run"]["one_action_landed"] = False
    assert_rc(plan, 1, tmp_path, "D3")


def test_strategy_needs_real_data(tmp_path):
    plan = load_good()
    plan["first_run"]["strategy_skill_ran"] = True
    plan["first_run"]["strategy_had_real_data"] = False
    assert_rc(plan, 1, tmp_path, "D3")


def test_strategy_needs_arbitrated_difference(tmp_path):
    plan = load_good()
    plan["first_run"]["differences_arbitrated"] = 0
    assert_rc(plan, 1, tmp_path, "D3")


# D4 定制四动作
def test_localization_done_needs_artifact(tmp_path):
    plan = load_good()
    plan["customization"]["localization"]["artifact"] = ""
    assert_rc(plan, 1, tmp_path, "D4")


def test_public_advisor_claims_must_be_sourced(tmp_path):
    plan = load_good()
    plan["customization"]["advisors"]["public_all_sourced"] = False
    assert_rc(plan, 1, tmp_path, "D4")


def test_private_advisor_claims_must_be_user_provided(tmp_path):
    plan = load_good()
    plan["customization"]["advisors"]["private_all_user_provided"] = False
    assert_rc(plan, 1, tmp_path, "D4")


def test_advisor_fabrication_test_must_pass(tmp_path):
    plan = load_good()
    plan["customization"]["advisors"]["fabrication_test_passed"] = False
    assert_rc(plan, 1, tmp_path, "D4")


def test_real_data_at_most_two_loops(tmp_path):
    plan = load_good()
    plan["customization"]["real_data"]["loops_picked"] = 3
    assert_rc(plan, 1, tmp_path, "D4")


def test_real_data_needs_one_closed_loop(tmp_path):
    plan = load_good()
    plan["customization"]["real_data"]["loops_closed"] = 0
    assert_rc(plan, 1, tmp_path, "D4")


def test_real_data_closure_needs_date_evidence(tmp_path):
    plan = load_good()
    plan["customization"]["real_data"]["closure_evidence_dated"] = False
    assert_rc(plan, 1, tmp_path, "D4")


def test_redlines_need_veto_entries(tmp_path):
    plan = load_good()
    plan["customization"]["redlines"]["veto_entries"] = 0
    assert_rc(plan, 1, tmp_path, "D4")


def test_redlines_must_be_machine_readable(tmp_path):
    plan = load_good()
    plan["customization"]["redlines"]["in_machine_readable_config"] = False
    assert_rc(plan, 1, tmp_path, "D4")


def test_not_done_action_needs_written_reason(tmp_path):
    plan = load_good()
    plan["customization"]["localization"]["done"] = False
    plan["customization"]["localization"]["artifact"] = ""
    assert_rc(plan, 1, tmp_path, "D4")


@pytest.mark.xfail(
    strict=True,
    reason="已知缺口：real_data.done=true 时没有要求 artifact/闭环证据路径；sample_good 自身 artifact 为空仍通过",
)
def test_real_data_done_requires_artifact(tmp_path):
    plan = load_good()
    plan["customization"]["real_data"]["artifact"] = ""
    assert_rc(plan, 1, tmp_path, "D4")


# D5 评估层
def test_no_long_term_skill_is_na(tmp_path):
    plan = load_good()
    plan["evaluation"]["skills_long_term"] = []
    assert_rc(plan, 0, tmp_path)


def test_evaluation_needs_baseline(tmp_path):
    plan = load_good()
    plan["evaluation"]["each_has_baseline"] = False
    assert_rc(plan, 1, tmp_path, "D5")


def test_evaluation_needs_metric(tmp_path):
    plan = load_good()
    plan["evaluation"]["each_has_metric"] = False
    assert_rc(plan, 1, tmp_path, "D5")


def test_evaluation_needs_regression(tmp_path):
    plan = load_good()
    plan["evaluation"]["each_has_regression"] = False
    assert_rc(plan, 1, tmp_path, "D5")


def test_regression_sample_needs_veto(tmp_path):
    plan = load_good()
    plan["evaluation"]["regression_sample_includes_veto"] = False
    assert_rc(plan, 1, tmp_path, "D5")


def test_evaluation_needs_two_scorecard_cycles(tmp_path):
    plan = load_good()
    plan["evaluation"]["scorecard_cycles"] = 1
    assert_rc(plan, 1, tmp_path, "D5")


# D6 机制抽取
def test_abstraction_needs_sop(tmp_path):
    plan = load_good()
    plan["abstraction"]["sop_written"] = False
    assert_rc(plan, 1, tmp_path, "D6")


def test_abstraction_needs_non_marketing_run(tmp_path):
    plan = load_good()
    plan["abstraction"]["non_marketing_runs"] = 0
    assert_rc(plan, 1, tmp_path, "D6")


def test_abstraction_needs_conflict_map(tmp_path):
    plan = load_good()
    plan["abstraction"]["conflict_map_complete"] = False
    assert_rc(plan, 1, tmp_path, "D6")


def test_unresolvable_must_be_marked_pending(tmp_path):
    plan = load_good()
    plan["abstraction"]["unresolvable_marked_pending"] = False
    assert_rc(plan, 1, tmp_path, "D6")


# D7 一致性
def test_installed_requires_fact_check(tmp_path):
    plan = load_good()
    plan["fact_check"]["star_trajectory"] = plan["fact_check"]["star_trajectory"][:2]
    assert_rc(plan, 1, tmp_path, "D7")


def test_strategy_requires_audit_first(tmp_path):
    plan = load_good()
    plan["first_run"]["audit_skill_first"] = False
    assert_rc(plan, 1, tmp_path, "D7")


def test_evaluation_requires_first_run(tmp_path):
    plan = load_good()
    plan["first_run"]["one_action_landed"] = False
    assert_rc(plan, 1, tmp_path, "D7")


@pytest.mark.xfail(
    strict=True,
    reason="已知缺口：嵌套类型错误没有 schema 守卫，契约要求 exit 2，实际 traceback + exit 1",
)
def test_malformed_fact_check_exit_2(tmp_path):
    plan = load_good()
    plan["fact_check"] = "oops"
    assert_rc(plan, 2, tmp_path)
