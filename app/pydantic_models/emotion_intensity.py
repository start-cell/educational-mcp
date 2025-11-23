"""Schemas for emotion intensity regression.

中文：情感强度回归接口的输入输出模型，定义文本与 0-1 分数。
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class IntensityRequest(BaseModel):
    text: str = Field(..., description="输入文本")


class IntensityResponse(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0, description="情感强度得分")
