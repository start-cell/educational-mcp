"""Schemas for deep cognitive diagnosis (e.g., DeepIRT-style) inference.

中文：深度认知诊断（DeepIRT 风格）输入输出模型，定义交互序列与掌握度格式。
"""

from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field


class Interaction(BaseModel):
    student_id: int = Field(..., description="学生 ID")
    item_id: int = Field(..., description="题目 ID")
    correct: int = Field(..., ge=0, le=1, description="是否答对，1/0")


class MasteryResponse(BaseModel):
    mastery: Dict[str, float] = Field(
        ..., description="知识点掌握概率，如 {'K1': 0.85}"
    )
    raw_vector: List[float] = Field(
        ..., description="模型输出的原始掌握向量，用于调试和可视化"
    )
