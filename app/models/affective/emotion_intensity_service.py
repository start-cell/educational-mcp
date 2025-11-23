"""Emotion intensity regression placeholder (RoBERTa-style API).

中文：情感强度回归占位实现，模拟 RoBERTa 风格接口，返回 0-1 分值。
"""

from __future__ import annotations

from math import tanh

from ...pydantic_models import IntensityResponse
from .sentiment_service import POSITIVE_WORDS, NEGATIVE_WORDS


def run_inference_intensity(text: str) -> IntensityResponse:
    """对输入文本计算情感强度得分（0~1）。"""
    pos_hits = sum(word in text for word in POSITIVE_WORDS)
    neg_hits = sum(word in text for word in NEGATIVE_WORDS)
    raw = pos_hits + neg_hits
    score = tanh(raw / 3.0)  # 映射为 0-1 内的平滑分数
    return IntensityResponse(score=round(score, 3))
