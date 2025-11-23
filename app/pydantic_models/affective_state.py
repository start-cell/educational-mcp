"""Schemas for the affective-state estimation mini-model.

中文：情感状态识别相关的 Pydantic 模型，用于请求校验与响应格式化。
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class AffectiveSignal(BaseModel):
    channel: str = Field(..., description="数据来源或信号类型，如 voice/keystroke")
    emotion: str = Field(..., description="检测到的情感标签")
    intensity: float = Field(..., ge=0.0, le=1.0, description="情感强度")
    evidence: Optional[str] = Field(default=None, description="辅助说明")


class AffectiveAnalysisRequest(BaseModel):
    student_id: str
    current_task: str
    affective_signals: List[AffectiveSignal]
    recent_performance: Optional[str] = Field(
        default=None, description="教师或系统记录的学习表现"
    )


class AffectiveState(BaseModel):
    dominant_emotion: str
    confidence: float
    message: str
    regulation_strategies: List[str]


class AffectiveAnalysisResponse(BaseModel):
    student_id: str
    state: AffectiveState
    nudges: List[str]
