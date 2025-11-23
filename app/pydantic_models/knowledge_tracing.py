"""Schemas powering the knowledge tracing mini-model.

中文：知识追踪接口的请求/响应模型，包含技能交互、掌握度与预测输出。
"""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SkillInteraction(BaseModel):
    skill: str = Field(..., description="知识技能名称")
    correct: bool = Field(..., description="是否答对")
    time_spent_seconds: Optional[int] = Field(
        default=None, description="作答耗时（秒）"
    )
    confidence: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="学生自评信心"
    )


class KnowledgeTracingRequest(BaseModel):
    student_id: str
    interactions: List[SkillInteraction]
    prior_mastery: Dict[str, float] = Field(
        default_factory=dict, description="先验掌握度，键为技能名，值为 0-1"
    )


class SkillProgress(BaseModel):
    skill: str
    probability_mastery: float
    trend: str
    next_action: str


class KnowledgeTracingResponse(BaseModel):
    student_id: str
    skills: List[SkillProgress]
    recommended_sequence: List[str]


# --- Advanced knowledge tracing (MRTKT / DKVMN-style) ---


class StudentInteraction(BaseModel):
    item_id: int = Field(..., description="题目 ID")
    correct: int = Field(..., ge=0, le=1, description="是否答对，1/0")
    timestamp: float = Field(..., description="时间戳或相对时间间隔")


class KTResponse(BaseModel):
    next_question_correct_prob: float = Field(
        ..., description="下一题答对的概率预测"
    )
    mastery: Dict[str, float] = Field(
        ..., description="当前各知识点掌握程度"
    )
