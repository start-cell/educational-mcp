"""Schemas for the keyword-based subjective grading mini-model.

中文：主观题评分的请求/响应模型，校验题目与作答字段并规范输出结构。
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class GradeAnswerRequest(BaseModel):
    question: str = Field(..., description="题目内容")
    correct_answer: str = Field(..., description="标准答案")
    student_answer: str = Field(..., description="学生作答")


class GradeAnswerResponse(BaseModel):
    is_correct: bool = Field(..., description="是否判定为正确")
    similarity: float = Field(..., ge=0.0, le=1.0, description="0～1 之间的覆盖率")
    matched_keywords: List[str] = Field(default_factory=list, description="命中的关键词")
    missing_keywords: List[str] = Field(default_factory=list, description="缺失的关键词")
    feedback: str = Field(..., description="自然语言反馈")
