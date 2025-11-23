"""Schemas for the study reflection-question generator.

中文：课后反思问题生成的请求/响应模型，校验反思深度与能力列表。
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, validator


class ReflectionRequest(BaseModel):
    lesson_title: str = Field(..., description="课程标题")
    skills_focus: Optional[List[str]] = Field(
        default=None, description="希望强调的能力列表"
    )
    difficulty: str = Field(
        "medium",
        description="反思题深度：easy/medium/hard",
    )

    @validator("difficulty")
    def _validate_difficulty(cls, value: str) -> str:
        level = value.lower()
        if level not in {"easy", "medium", "hard"}:
            raise ValueError("difficulty 必须是 easy/medium/hard")
        return level


class ReflectionResponse(BaseModel):
    lesson_title: str
    difficulty: str
    questions: List[str]
