"""Schemas for sentence-level sentiment classification.

中文：整体情感分类的输入输出模型，定义文本与概率标签字段。
"""

from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, Field


class SentimentRequest(BaseModel):
    text: str = Field(..., description="待分析文本")


class SentimentResponse(BaseModel):
    probabilities: Dict[str, float] = Field(
        ..., description="各情感类别的概率"
    )
    label: str = Field(..., description="预测情感标签")
