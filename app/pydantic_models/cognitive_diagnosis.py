"""Schemas for the cognitive diagnosis diagnostic mini-model.

中文：认知诊断相关的数据结构，定义概念快照、诊断结果与整体输出格式。
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ConceptSnapshot(BaseModel):
    concept_name: str = Field(..., description="知识概念名称")
    attempts: int = Field(..., gt=0, description="累计作答次数")
    correct: int = Field(..., ge=0, description="作答正确次数")
    misconceptions: List[str] = Field(
        default_factory=list, description="暴露出的典型错误或概念偏差"
    )

    @property
    def mastery(self) -> float:
        return min(max(self.correct / self.attempts, 0.0), 1.0)


class CognitiveDiagnosisRequest(BaseModel):
    student_id: str
    subject: str
    concept_snapshots: List[ConceptSnapshot]
    recent_behaviors: Optional[List[str]] = Field(
        default=None, description="教师观察到的行为标签"
    )


class ConceptDiagnosis(BaseModel):
    concept_name: str
    mastery: float
    level: str
    misconceptions: List[str]
    recommendation: str


class CognitiveDiagnosisResponse(BaseModel):
    student_id: str
    subject: str
    overall_mastery: float
    strengths: List[str]
    risks: List[str]
    concepts: List[ConceptDiagnosis]
    summary: str
