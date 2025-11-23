"""Affective computing and sentiment services.

中文：情感识别与情感分析相关的业务逻辑集合。"""

from .affective_state_service import analyze_affective_state
from .sentiment_service import run_inference_sentiment
from .aspect_sentiment_service import run_inference_aspect_sentiment
from .emotion_intensity_service import run_inference_intensity

__all__ = [
    "analyze_affective_state",
    "run_inference_sentiment",
    "run_inference_aspect_sentiment",
    "run_inference_intensity",
]
