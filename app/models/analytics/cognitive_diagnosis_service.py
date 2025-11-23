"""Rule-based cognitive diagnosis engine.

中文：认知诊断业务层，基于概念掌握度和行为生成分级、风险与建议。
"""

from __future__ import annotations

from statistics import mean
from typing import List

from ...models import (
    CognitiveDiagnosisRequest,
    CognitiveDiagnosisResponse,
    ConceptDiagnosis,
    ConceptSnapshot,
)


def _level_from_mastery(mastery: float) -> str:
    if mastery >= 0.85:
        return "稳定掌握"
    if mastery >= 0.65:
        return "发展中"
    return "高风险"


def _recommendation(snapshot: ConceptSnapshot, mastery: float) -> str:
    if mastery >= 0.85:
        return "通过挑战性任务保持迁移练习。"
    if mastery >= 0.65:
        focus = snapshot.misconceptions[0] if snapshot.misconceptions else "易错点"
        return f"安排变式练习，突出对比 {focus}。"
    return "回到概念本源，结合具体例子重新建模。"


def diagnose_cognition(payload: CognitiveDiagnosisRequest) -> CognitiveDiagnosisResponse:
    concepts: List[ConceptDiagnosis] = []
    strengths: List[str] = []
    risks: List[str] = []

    for snapshot in payload.concept_snapshots:
        mastery = round(snapshot.mastery, 3)
        level = _level_from_mastery(mastery)
        if level == "稳定掌握":
            strengths.append(snapshot.concept_name)
        elif level == "高风险":
            risks.append(snapshot.concept_name)
        concepts.append(
            ConceptDiagnosis(
                concept_name=snapshot.concept_name,
                mastery=mastery,
                level=level,
                misconceptions=snapshot.misconceptions,
                recommendation=_recommendation(snapshot, mastery),
            )
        )

    overall_mastery = round(
        mean([concept.mastery for concept in payload.concept_snapshots]) if payload.concept_snapshots else 0.0,
        3,
    )

    behavior_note = ""
    if payload.recent_behaviors:
        behavior_note = f"行为观察：{'、'.join(payload.recent_behaviors)}。"

    summary = (
        f"{payload.student_id} 在 {payload.subject} 中整体掌握度约为 {overall_mastery:.0%}。"
        f"优势概念：{', '.join(strengths) or '暂未形成亮点'}；"
        f"风险概念：{', '.join(risks) or '暂无'}。"
        f"{behavior_note}"
    )

    return CognitiveDiagnosisResponse(
        student_id=payload.student_id,
        subject=payload.subject,
        overall_mastery=overall_mastery,
        strengths=strengths,
        risks=risks,
        concepts=concepts,
        summary=summary,
    )
