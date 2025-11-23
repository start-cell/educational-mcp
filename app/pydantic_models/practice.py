"""Schemas powering the personalised practice-plan generator.

中文：练习计划接口的数据模型，定义主题、薄弱点、阶段活动等字段。
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class PracticePlanRequest(BaseModel):
    topic: str = Field(..., description="学习主题")
    student_level: str = Field(..., description="学生水平，例如 初一/中级")
    weak_points: List[str] = Field(default_factory=list, description="薄弱知识点列表")
    available_minutes: int = Field(30, gt=0, description="可用时间（分钟）")


class PracticePhase(BaseModel):
    name: str
    duration_minutes: int
    activities: List[str]


class PracticePlanResponse(BaseModel):
    topic: str
    student_level: str
    total_minutes: int
    weak_points: List[str]
    phases: List[PracticePhase]
