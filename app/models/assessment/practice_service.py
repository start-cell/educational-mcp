"""Personalised practice plan builder.

中文：个性化练习计划业务逻辑，生成分阶段活动与时间分配。
"""

from __future__ import annotations

from typing import List

from ...pydantic_models import PracticePhase, PracticePlanRequest, PracticePlanResponse


def build_practice_plan(payload: PracticePlanRequest) -> PracticePlanResponse:
    weak_points = [item.strip() for item in payload.weak_points if item.strip()]
    segment = max(payload.available_minutes // 3, 5)

    phases: List[PracticePhase] = [
        PracticePhase(
            name="回顾核心概念",
            duration_minutes=segment,
            activities=[
                f"用思维导图复盘「{payload.topic}」相关定义",
                "找出与薄弱点相关的两个例子",
            ],
        ),
        PracticePhase(
            name="针对性练习",
            duration_minutes=segment,
            activities=[
                "完成 2-3 道示例题，记录错误原因",
            ],
        ),
        PracticePhase(
            name="迁移与反思",
            duration_minutes=payload.available_minutes - 2 * segment,
            activities=[
                "尝试一道综合拓展题，写出解题步骤",
                "总结保留问题与改进策略",
            ],
        ),
    ]

    if weak_points:
        phases[1].activities.insert(0, f"优先攻克：{', '.join(weak_points)}")

    return PracticePlanResponse(
        topic=payload.topic,
        student_level=payload.student_level,
        total_minutes=payload.available_minutes,
        weak_points=weak_points,
        phases=phases,
    )
