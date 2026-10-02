#!/usr/bin/env python3
"""validate.py — skill-lib-iterate 开源 Skill 库迭代计划七维校验器

输入: Skill 库迭代计划 JSON（schema 见 tests/sample_good.json）
  {
    "fact_check": {                          // 第 0 步：事实核对（N1-N4）
      "star_trajectory": [                   // N1：≥3 个时间锚点（仅快照=话术风险）
        {"t": "v2.6.0前后", "stars_k": 32.9},
        {"t": "2026-07", "stars_k": 39.4},
        {"t": "2026-09", "stars_k": 47.1}
      ],
      "actual_scale": 47,                    // N2：库实际 Skill 数（非宣传数）
      "advertised_scale": 4,                 // 宣传清单数
      "scenario_related": ["cro", "seo-audit", "marketing-loops", "pricing"],
      "simulation_guardrail_quoted": true,   // N3：模拟类 Skill 护栏原文已摘录
      "eval_limits_mapped": true             // N4：评测限制项已转迭代必做项
    },
    "foundation": {                          // L1-① 产品上下文底座
      "positioning": "X 是给 5-50 人 SaaS 团队的中文 AI 搜索优化工具，解决内容在 DeepSeek/豆包不被引用的问题",
      "audience": "行业:SaaS | 角色:市场负责人(买)+内容运营(用) | 规模:5-50人 | 痛点:内容投入大但 AI 渠道零引用",
      "value_prop": "同样内容引用率是人工优化 3 倍（可验证）",
      "alternatives": ["竞品A(英文市场)", "人工优化(贵且慢)", "什么都不做(引用率维持 0)"],
      "replacement_test_passed": true,       // 替换测试：产品名可替换仍成立=套话(须 false 才算过? 不：true=每条都过)
      "pending_fields": 0                    // "待定/TBD" 字段数（必须 0）
    },
    "first_run": {                           // L1-② 安装与首跑
      "installed": true,
      "audit_skill_first": true,             // 先跑审计型（cro/seo-audit）
      "audit_actionable_items": 4,           // 审计产出可执行改动（≥3，每条含改哪里/怎么改/为什么）
      "one_action_landed": true,             // 落地了 1 条（留改前/改后对比）
      "strategy_skill_ran": true,            // 战略讨论型（council）已跑
      "strategy_had_real_data": true,        // 战略讨论前置=手里有真实数据（false=空转违规）
      "differences_arbitrated": 1            // 分歧地图中用现有证据裁决的分歧数（≥1）
    },
    "customization": {                       // L2 定制四动作（做=有产物，不做=书面理由）
      "localization": {"done": true, "artifact": "渠道×结构偏好映射表（5 渠道实测）+ 改造后 ai-seo 配置"},
      "advisors": {
        "done": true,
        "artifact": "12 位顾问清单（身份类型+框架要点+出处）+ 冲突自检 3 题",
        "public_all_sourced": true,          // 公众人物观点全部可溯源（任一编造=false）
        "private_all_user_provided": true,   // 私有顾问观点全部由用户提供（AI 编造=false）
        "fabrication_test_passed": true      // 编造测试：未提供立场未被生成（护栏生效）
      },
      "real_data": {
        "done": true,
        "loops_picked": 2,                   // 1-2 个 loop（>2=同时上多个，无法归因）
        "loops_closed": 1,                   // 已跑通完整闭环数（"配置好了"≠跑通）
        "closure_evidence_dated": true       // 闭环留档带真实日期与真实触发
      },
      "redlines": {
        "done": true,
        "veto_entries": 5,                   // veto list 条目数（≥1）
        "in_machine_readable_config": true   // 写进 Skill 配置（非 README/记忆）
      }
    },
    "evaluation": {                          // L3-e 效果评估层（它没做的空位）
      "skills_long_term": ["seo-audit", "council"],
      "each_has_baseline": true,             // 每个长期 Skill 有采用前基线
      "each_has_metric": true,               // 每个有归因/辅助指标（标注归因性）
      "each_has_regression": true,           // 每个有回归测试（固定样例+期望+判定）
      "regression_sample_includes_veto": true, // 回归样例含 1 个该被 veto 的输入
      "scorecard_cycles": 2,                 // 跑分周期数（≥2 才能谈趋势）
      "retirement_review_done": true         // 触发过淘汰评审则已做记录
    },
    "abstraction": {                         // L3-f 机制抽取（分歧地图通用化）
      "sop_written": true,                   // 决策 SOP 模板（视角/独立输出/分歧地图/证据裁决）
      "non_marketing_runs": 1,               // 非营销场景跑完次数（≥1）
      "conflict_map_complete": true,         // 分歧地图四步产物齐全
      "unresolvable_marked_pending": true    // 裁决不了的标了"待补证据"（未硬裁决）
    }
  }

七维校验（任一 FAIL → exit 1）：
  D1 事实核对: star_trajectory ≥3 个锚点（仅快照=话术风险，拦截）且数值非递减
     异常不拦（尖峰允许，但 ≥3 点必须有）；actual_scale ≥ advertised_scale
     （实际 < 宣传 = 宣传有幻觉）；scenario_related 非空（N2 筛查做了）；
     simulation_guardrail_quoted 与 eval_limits_mapped 均 true
  D2 底座: 四要素（positioning/audience/value_prop/alternatives）全部非空
     且 pending_fields=0（"待定"=底座未完成）且 replacement_test_passed=true
     且 alternatives 含"什么都不做"（最强竞品没写 = 受众痛感没想清）
  D3 首跑顺序: audit_skill_first=true（先审计型）且 audit_actionable_items ≥3
     且 one_action_landed=true（没落地=验证停在"看起来有用"）；
     strategy_skill_ran=true 时须 strategy_had_real_data=true（没数据跑战略型=空转）
     且 differences_arbitrated ≥1（分歧没被证据裁决 = 机制没真跑）
  D4 定制: 四动作各 done=true 时产物齐（localization.artifact 非空 /
     advisors 三项护栏全 true——public_all_sourced+private_all_user_provided+
     fabrication_test_passed，任一 false=编造红线 / real_data: loops_picked 1-2
     且 loops_closed ≥1 且闭环留档带日期 / redlines: veto_entries ≥1 且
     in_machine_readable_config=true）；done=false 的动作 artifact 须有
     书面理由（非空）——"不做"也要留痕
  D5 评估层: 每个长期 Skill 三件齐（baseline+metric+regression 均 true）
     且 regression_sample_includes_veto=true（样例不含该被拦的 = 回归测不到护栏）
     且 scorecard_cycles ≥2（1 个周期没有趋势）；skills_long_term 为空 = 评估层 N/A
  D6 机制抽取: sop_written=true 且 non_marketing_runs ≥1
     且 conflict_map_complete=true 且 unresolvable_marked_pending=true
     （裁决不了先综合 = 机制被滥用为权威感掩盖信息缺失，拦截）
  D7 一致性: first_run.installed=true 须 fact_check 四道全过
     （核对没完成就安装 = 在话术上盖楼）；
     strategy_skill_ran=true 须 audit_skill_first=true 且 audit_actionable_items ≥3
     （审计型没跑通就上战略型 = 顺序反了）；
     evaluation 生效（skills_long_term 非空）须 first_run 首跑验收过
     （没跑通就先谈评估 = 无米之炊）

退出码：0=通过 / 1=有缺陷 / 2=文件/格式错误
"""
import json
import sys


def fail(checks, code, msg):
    checks.append(("FAIL", code, msg))


def ok(checks, code, msg):
    checks.append(("OK", code, msg))


def is_nonempty_str(v):
    return isinstance(v, str) and v.strip() != ""


def validate(plan):
    checks = []

    fc = plan.get("fact_check") or {}
    fd = plan.get("foundation") or {}
    fr = plan.get("first_run") or {}
    cu = plan.get("customization") or {}
    ev = plan.get("evaluation") or {}
    ab = plan.get("abstraction") or {}

    # D1 事实核对
    traj = fc.get("star_trajectory") or []
    actual = fc.get("actual_scale")
    advert = fc.get("advertised_scale")
    related = fc.get("scenario_related") or []
    if not isinstance(traj, list) or len(traj) < 3:
        fail(checks, "D1", f"star_trajectory 仅 {len(traj) if isinstance(traj, list) else 0} 个锚点——"
                           "≥3 个时间点才有斜率；仅快照=话术风险，引用必须带时间戳")
    else:
        vals = [p.get("stars_k") for p in traj]
        if not all(isinstance(v, (int, float)) for v in vals):
            fail(checks, "D1", f"star_trajectory 数值非法: {vals}——锚点必须是 Star 数字")
        elif not all(is_nonempty_str(p.get("t")) for p in traj):
            fail(checks, "D1", "star_trajectory 锚点缺时间点——'42.9K'不带时间戳=裸数字禁用")
        else:
            if not (isinstance(actual, int) and isinstance(advert, int) and actual >= advert):
                fail(checks, "D1", f"实际规模 {actual!r} vs 宣传 {advert!r}——"
                                   "实际 < 宣传 = 宣传有幻觉；决策须基于全量清单")
            elif not related:
                fail(checks, "D1", "scenario_related 为空——N2 全量清单没按场景筛（宣传清单≠全量）")
            elif fc.get("simulation_guardrail_quoted") is not True:
                fail(checks, "D1", "simulation_guardrail_quoted=false——模拟类 Skill 护栏原文没摘录（没读=凭印象）")
            elif fc.get("eval_limits_mapped") is not True:
                fail(checks, "D1", "eval_limits_mapped=false——评测点名的限制没转成迭代必做项（限制=前置不是可选项）")
            else:
                ok(checks, "D1", f"事实核对合规（{len(traj)} 个 Star 锚点 + 规模 {actual}/{advert} + 场景相关 {len(related)} 项）")

    # D2 底座
    four = ("positioning", "audience", "value_prop")
    pend = fd.get("pending_fields")
    alts = fd.get("alternatives") or []
    if not all(is_nonempty_str(fd.get(k)) for k in four):
        missing = [k for k in four if not is_nonempty_str(fd.get(k))]
        fail(checks, "D2", f"底座四要素缺: {missing}——底座未完成禁止首跑（输出必是通用套话）")
    elif not is_nonempty_str_list_check(alts):
        fail(checks, "D2", "alternatives 为空——竞品替代没写（含'什么都不做'——最强竞品）")
    elif not any(("什么都不做" in a) or ("not buy" in a.lower()) or ("do nothing" in a.lower()) for a in alts):
        fail(checks, "D2", "alternatives 没含'什么都不做'——用户为什么忍着不买没想清 = 痛感强度未知")
    elif pend != 0:
        fail(checks, "D2", f"pending_fields={pend}——底座里有'待定/TBD'（待定=没想清，回去想清再进首跑）")
    elif fd.get("replacement_test_passed") is not True:
        fail(checks, "D2", "replacement_test_passed=false——替换测试没过：产品名可替换仍成立=套话底座")
    else:
        ok(checks, "D2", "底座完成（四要素非空 + 替换测试过 + 含'什么都不做' + 零待定）")

    # D3 首跑顺序
    audit_items = fr.get("audit_actionable_items")
    strat_ran = fr.get("strategy_skill_ran") is True
    if fr.get("audit_skill_first") is not True:
        fail(checks, "D3", "audit_skill_first=false——没先跑审计型（先真实改动后战略讨论，顺序反了）")
    elif not isinstance(audit_items, int) or audit_items < 3:
        fail(checks, "D3", f"audit_actionable_items={audit_items!r}——审计产出可执行改动 <3 条（Skill 没读到现状）")
    elif fr.get("one_action_landed") is not True:
        fail(checks, "D3", "one_action_landed=false——没落地 1 条（验证停在'看起来有用'，要留改前/改后对比）")
    else:
        if strat_ran and fr.get("strategy_had_real_data") is not True:
            fail(checks, "D3", "strategy_had_real_data=false——没数据跑战略讨论型=对着空气分析（空转）")
        elif strat_ran and not (isinstance(fr.get("differences_arbitrated"), int)
                                and fr.get("differences_arbitrated") >= 1):
            fail(checks, "D3", f"differences_arbitrated={fr.get('differences_arbitrated')!r}——"
                               "分歧没被证据裁决（机制没真跑，'通常来说'式裁决=稻草人）")
        else:
            extra = f"；战略型已跑（真实数据+裁决 {fr.get('differences_arbitrated')} 个分歧）" if strat_ran else "；战略型未跑（合规：前置未齐）"
            ok(checks, "D3", f"首跑顺序合规（审计型先跑，{audit_items} 条改动，落地 1 条{extra}）")

    # D4 定制四动作
    bad_cu = []
    loc = cu.get("localization") or {}
    adv = cu.get("advisors") or {}
    rd = cu.get("real_data") or {}
    rl = cu.get("redlines") or {}
    if loc.get("done") is True:
        if not is_nonempty_str(loc.get("artifact")):
            bad_cu.append("localization(做了没产物——映射表/改造配置呢？)")
    elif not is_nonempty_str(loc.get("artifact")):
        bad_cu.append("localization(不做也没书面理由——取舍要留痕)")
    if adv.get("done") is True:
        if not is_nonempty_str(adv.get("artifact")):
            bad_cu.append("advisors(做了没产物——顾问清单/冲突自检呢？)")
        elif adv.get("public_all_sourced") is not True:
            bad_cu.append("advisors(公众人物观点有不可溯源的——溯源不到=在你的系统里等价于编造)")
        elif adv.get("private_all_user_provided") is not True:
            bad_cu.append("advisors(私有顾问观点非你提供——AI 替真人表态=红线事故，责任在你)")
        elif adv.get("fabrication_test_passed") is not True:
            bad_cu.append("advisors(编造测试没过——'未提供立场'被生成了，护栏没生效)")
    elif not is_nonempty_str(adv.get("artifact")):
        bad_cu.append("advisors(不做也没书面理由)")
    if rd.get("done") is True:
        lp = rd.get("loops_picked")
        lc = rd.get("loops_closed")
        if not (isinstance(lp, int) and 1 <= lp <= 2):
            bad_cu.append(f"real_data(loops_picked={lp!r}——一次最多 2 个，>2 无法归因)")
        elif not (isinstance(lc, int) and lc >= 1):
            bad_cu.append(f"real_data(loops_closed={lc!r}——'配置好了'≠'跑通了'，至少 1 个完整闭环)")
        elif rd.get("closure_evidence_dated") is not True:
            bad_cu.append("real_data(闭环没留档带真实日期/真实触发——手动模拟跑的不算闭环)")
    elif not is_nonempty_str(rd.get("artifact")):
        bad_cu.append("real_data(不做也没书面理由——例：数据源还没打通(打通时间:__？)")
    if rl.get("done") is True:
        ve = rl.get("veto_entries")
        if not (isinstance(ve, int) and ve >= 1):
            bad_cu.append(f"redlines(veto_entries={ve!r}——红线 0 条=没加)")
        elif rl.get("in_machine_readable_config") is not True:
            bad_cu.append("redlines(veto 没写进 Skill 机器可读配置——写在 README/记忆里=veto 不存在)")
    elif not is_nonempty_str(rl.get("artifact")):
        bad_cu.append("redlines(不做也没书面理由——例：行业无特殊合规(已查清单:__？)")
    if bad_cu:
        fail(checks, "D4", "定制四动作: " + "；".join(bad_cu))
    else:
        done_n = sum(x.get("done") is True for x in (loc, adv, rd, rl))
        ok(checks, "D4", f"定制合规（{done_n}/4 动作做了且产物齐，未做的有书面理由）")

    # D5 评估层
    st = ev.get("skills_long_term") or []
    if not st:
        ok(checks, "D5", "无长期采用 Skill（评估层暂不适用——采用 ≥1 个 Skill 满 1 周期后启用）")
    else:
        if ev.get("each_has_baseline") is not True:
            fail(checks, "D5", "each_has_baseline=false——没采采用前基线，'提升'无从谈起（先采基线再用，不是用完补采）")
        elif ev.get("each_has_metric") is not True:
            fail(checks, "D5", "each_has_metric=false——没有归因/辅助指标，Skill 在'裸跑'（看起来专业≠在产生价值）")
        elif ev.get("each_has_regression") is not True:
            fail(checks, "D5", "each_has_regression=false——没有回归测试，你改配置/升级后不知道它变没变差")
        elif ev.get("regression_sample_includes_veto") is not True:
            fail(checks, "D5", "regression_sample_includes_veto=false——回归样例不含该被 veto 的输入（护栏失效测不到）")
        elif not (isinstance(ev.get("scorecard_cycles"), int) and ev.get("scorecard_cycles") >= 2):
            fail(checks, "D5", f"scorecard_cycles={ev.get('scorecard_cycles')!r}——<2 个周期没有趋势（趋势是淘汰机制的依据）")
        else:
            ok(checks, "D5", f"评估层合规（{len(st)} 个长期 Skill × 基线+指标+回归，跑分 {ev['scorecard_cycles']} 周期）")

    # D6 机制抽取
    if ab.get("sop_written") is not True:
        fail(checks, "D6", "sop_written=false——分歧地图决策 SOP 没写（视角/独立输出/分歧归框架/证据裁决四步模板）")
    elif not (isinstance(ab.get("non_marketing_runs"), int) and ab.get("non_marketing_runs") >= 1):
        fail(checks, "D6", f"non_marketing_runs={ab.get('non_marketing_runs')!r}——非营销场景没跑完 ≥1 次（营销里跑通≠抽取成功）")
    elif ab.get("conflict_map_complete") is not True:
        fail(checks, "D6", "conflict_map_complete=false——分歧地图四步产物不齐（视角/独立输出/分歧归框架/裁决或待补）")
    elif ab.get("unresolvable_marked_pending") is not True:
        fail(checks, "D6", "unresolvable_marked_pending=false——裁决不了的先综合了=机制被滥用为'权威感掩盖信息缺失'"
                           "（比不用更危险）")
    else:
        ok(checks, "D6", f"机制抽取合规（SOP + 非营销场景 {ab['non_marketing_runs']} 次 + 分歧地图齐全 + 待补证据已标注）")

    # D7 一致性
    issues = []
    fact_ok = (isinstance(traj, list) and len(traj) >= 3
               and all(isinstance(p.get("stars_k"), (int, float)) and is_nonempty_str(p.get("t")) for p in traj)
               and isinstance(actual, int) and isinstance(advert, int) and actual >= advert
               and bool(related)
               and fc.get("simulation_guardrail_quoted") is True
               and fc.get("eval_limits_mapped") is True)
    if fr.get("installed") is True and not fact_ok:
        issues.append("已安装但事实核对（N1-N4）未全过——在话术上盖楼")
    if strat_ran and not (fr.get("audit_skill_first") is True
                          and isinstance(audit_items, int) and audit_items >= 3):
        issues.append("战略讨论型已跑但审计型未验收（先真实改动后战略讨论，顺序反了）")
    if st and not (fr.get("audit_skill_first") is True
                   and isinstance(audit_items, int) and audit_items >= 3
                   and fr.get("one_action_landed") is True):
        issues.append("评估层已启用但首跑验收未过——没跑通就谈评估=无米之炊")
    if issues:
        fail(checks, "D7", "一致性: " + "；".join(issues))
    else:
        ok(checks, "D7", "一致性合规（核对→底座→首跑→定制→评估→抽取，前置链完整）")

    return checks


def is_nonempty_str_list(v):
    return isinstance(v, list) and any(is_nonempty_str(x) for x in v)


def is_nonempty_str_list_check(v):
    return is_nonempty_str_list(v)


def main():
    if len(sys.argv) != 2:
        print("usage: python validate.py plan.json", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            plan = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: 无法读取/解析: {e}", file=sys.stderr)
        return 2
    if not isinstance(plan, dict):
        print("ERROR: 顶层必须是 JSON 对象", file=sys.stderr)
        return 2

    checks = validate(plan)
    fails = [c for c in checks if c[0] == "FAIL"]
    for status, code, msg in checks:
        if status == "FAIL":
            print(f"[{code}] FAIL {msg}")
    print(f"== {len(checks) - len(fails)} OK / {len(fails)} FAIL ==")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
