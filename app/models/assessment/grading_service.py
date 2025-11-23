"""Keyword coverage scorer for subjective answers.

中文：主观题评分规则层，基于关键词覆盖率计算得分与反馈（不含框架/路由逻辑）。
"""

from __future__ import annotations

from typing import Dict, List, Sequence

from ...pydantic_models import GradeAnswerRequest, GradeAnswerResponse


def _tokenize(text: str) -> List[str]:
    return [
        token
        for token in text.lower().replace("，", " ").replace("。", " ").split()
        if token
    ]


def _keyword_stats(std_tokens: Sequence[str], stu_tokens: Sequence[str]) -> Dict[str, List[str]]:
    std_set = set(std_tokens)
    stu_set = set(stu_tokens)
    overlap = sorted(std_set.intersection(stu_set))
    missing = sorted(std_set - set(overlap))
    return {"matched": overlap, "missing": missing}


def score_answer(payload: GradeAnswerRequest) -> GradeAnswerResponse:
    std_tokens = _tokenize(payload.correct_answer)
    stu_tokens = _tokenize(payload.student_answer)
    stats = _keyword_stats(std_tokens, stu_tokens)
    coverage = len(stats["matched"]) / max(len(std_tokens), 1)
    similarity = round(coverage, 3)

    if not payload.student_answer.strip():
        feedback = "系统未检测到作答，可提醒学生先尝试回答。"
    elif similarity >= 0.9:
        feedback = "作答内容非常完整，与标准答案高度一致。"
    elif similarity >= 0.7:
        feedback = "作答基本正确，可以补充缺失关键词以更全面。"
    elif similarity >= 0.4:
        feedback = "部分要点正确，建议强化缺失的概念。"
    else:
        feedback = "与标准答案差距较大，可引导学生重新审题并列出要点。"

    return GradeAnswerResponse(
        is_correct=similarity >= 0.7,
        similarity=similarity,
        matched_keywords=stats["matched"],
        missing_keywords=stats["missing"],
        feedback=feedback,
    )
