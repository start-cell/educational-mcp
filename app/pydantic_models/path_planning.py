"""Schemas for personalized learning path planning.

中文：学习路径推荐的请求/响应模型，描述掌握度输入与推荐列表输出。
"""

from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field


class PathRequest(BaseModel):
    mastery: Dict[str, float] = Field(
        ..., description="学生掌握度字典，如 {'K1': 0.5}"
    )
    threshold: float = Field(
        default=0.7, ge=0.0, le=1.0, description="低于阈值视为未掌握"
    )
    max_recommend: int = Field(
        default=5, gt=0, description="最多推荐的知识点数量"
    )


class PathResponse(BaseModel):
    recommended_path: List[str] = Field(
        ..., description="推荐的学习路径（知识点 ID 列表）"
    )
