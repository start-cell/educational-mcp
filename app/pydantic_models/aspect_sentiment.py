"""Schemas for aspect-level sentiment classification.

中文：方面级情感分析的请求/响应模型，记录文本、方面列表与预测标签。
"""

from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field


class AspectSentimentRequest(BaseModel):
    text: str = Field(..., description="输入文本")
    aspects: List[str] = Field(..., description="要分析的方面列表")


class AspectSentimentResponse(BaseModel):
    aspect_results: Dict[str, str] = Field(
        ..., description="每个方面的情感标签"
    )
