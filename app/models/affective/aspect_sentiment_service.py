"""Aspect-level sentiment analysis placeholder.

中文：方面级情感分析占位实现，复用情感打分逻辑输出各方面标签。
"""

from __future__ import annotations

from typing import Dict, List

from ...models import AspectSentimentResponse
from .sentiment_service import _simple_score


def run_inference_aspect_sentiment(text: str, aspects: List[str]) -> AspectSentimentResponse:
    """对指定方面进行情感分析。"""
    aspect_results: Dict[str, str] = {}
    base_probs = _simple_score(text)
    for aspect in aspects:
        # 简化：直接沿用整体情感作为各方面结果
        label = max(base_probs.items(), key=lambda x: x[1])[0]
        aspect_results[aspect] = label
    return AspectSentimentResponse(aspect_results=aspect_results)
