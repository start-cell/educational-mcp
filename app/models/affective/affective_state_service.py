"""Simple affect-aware coach that blends multimodal signals.

中文：情感状态分析业务层，融合多模态信号并给出调节建议，独立于路由。
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

from ...pydantic_models import (
    AffectiveAnalysisRequest,
    AffectiveAnalysisResponse,
    AffectiveSignal,
    AffectiveState,
)


def _aggregate_emotions(signals: List[AffectiveSignal]) -> Tuple[str, float]:
    weights: Dict[str, float] = defaultdict(float)
    for sig in signals:
        weights[sig.emotion.lower()] += sig.intensity
    if not weights:
        return "neutral", 0.2
    dominant = max(weights.items(), key=lambda item: item[1])
    total = sum(weights.values())
    confidence = dominant[1] / total if total else 0.0
    return dominant[0], round(confidence, 3)


def _strategies(emotion: str) -> List[str]:
    if emotion in {"frustration", "anxious", "stress"}:
        return [
            "给出分步提示并降低任务难度。",
            "安排 2 分钟呼吸或伸展休息。",
        ]
    if emotion in {"bored", "disengaged"}:
        return [
            "引入情境化问题提升意义感。",
            "设置限时小挑战提高专注度。",
        ]
    if emotion in {"confident", "excited"}:
        return [
            "提供扩展任务鼓励探索。",
            "邀请学生向同伴讲解巩固知识。",
        ]
    return [
        "询问学生状态，给予定制化支持。",
        "对当前努力给予正向反馈。",
    ]


def analyze_affective_state(payload: AffectiveAnalysisRequest) -> AffectiveAnalysisResponse:
    dominant_emotion, confidence = _aggregate_emotions(payload.affective_signals)

    if dominant_emotion in {"frustration", "anxious"}:
        message = f"检测到 {payload.student_id} 在「{payload.current_task}」中可能感到挫折。建议先处理最关键步骤。"
    elif dominant_emotion in {"bored"}:
        message = f"{payload.student_id} 的情绪趋于低唤醒，可尝试切换更具挑战性的子任务。"
    elif dominant_emotion in {"confident", "excited"}:
        message = f"{payload.student_id} 状态积极，可趁势加入举一反三的问题。"
    else:
        message = f"{payload.student_id} 情绪较为平稳，保持当前节奏并轻量检查理解情况。"

    if payload.recent_performance:
        message += f" 学习表现备注：{payload.recent_performance}。"

    state = AffectiveState(
        dominant_emotion=dominant_emotion,
        confidence=confidence,
        message=message,
        regulation_strategies=_strategies(dominant_emotion),
    )

    nudges = [
        "使用 1-2 句同理心话语回应学生感受。",
        f"根据情绪状态对「{payload.current_task}」调整脚手架层级。",
    ]

    return AffectiveAnalysisResponse(
        student_id=payload.student_id,
        state=state,
        nudges=nudges,
    )
