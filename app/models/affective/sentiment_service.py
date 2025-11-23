"""Lightweight sentiment classifier placeholder for BiLSTM+Attention pipeline.

中文：情感分类占位实现，模拟 BiLSTM+Attention 形式的接口，提供概率与标签。
"""

from __future__ import annotations

from typing import Dict

from ...models import SentimentResponse

POSITIVE_WORDS = {"好", "满意", "喜欢", "清晰", "有趣", "赞", "棒"}
NEGATIVE_WORDS = {"差", "糟", "难", "晦涩", "失望", "生气", "不满"}
CATEGORIES = ["负面", "中性", "正面"]


def _simple_score(text: str) -> Dict[str, float]:
    pos_hits = sum(word in text for word in POSITIVE_WORDS)
    neg_hits = sum(word in text for word in NEGATIVE_WORDS)
    total = pos_hits + neg_hits
    if total == 0:
        return {"负面": 0.2, "中性": 0.6, "正面": 0.2}
    pos_prob = pos_hits / total
    neg_prob = neg_hits / total
    return {
        "负面": round(0.1 + 0.8 * neg_prob, 3),
        "中性": 0.1,
        "正面": round(0.1 + 0.8 * pos_prob, 3),
    }


def run_inference_sentiment(text: str) -> SentimentResponse:
    """对输入文本进行情感分析（简化版）。"""
    prob_dict = _simple_score(text)
    label = max(prob_dict.items(), key=lambda x: x[1])[0]
    return SentimentResponse(probabilities=prob_dict, label=label)
