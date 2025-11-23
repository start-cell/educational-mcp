"""Reflection question generator for post-lesson metacognition.

中文：反思问题生成器，按照难度和关注能力输出题目列表，与 API 解耦。
"""

from __future__ import annotations

from typing import Dict, List

from ...pydantic_models import ReflectionRequest, ReflectionResponse


def generate_reflections(payload: ReflectionRequest) -> ReflectionResponse:
    base_questions: Dict[str, List[str]] = {
        "easy": [
            "今天学到的最重要概念是什么？",
            "用自己的话复述一个课堂例子。",
        ],
        "medium": [
            "本课知识与之前内容有什么联系？",
            "如果向同学讲授这个内容，你会怎么安排步骤？",
        ],
        "hard": [
            "当遇到相关题目时，你最容易出错的环节是什么？如何避免？",
            "设计一道新题检验该知识点，并写出答案。",
        ],
    }

    questions: List[str] = list(base_questions[payload.difficulty])
    if payload.skills_focus:
        questions.extend(
            f"在本课中，你如何体现「{skill}」这一能力？"
            for skill in payload.skills_focus
        )

    return ReflectionResponse(
        lesson_title=payload.lesson_title,
        difficulty=payload.difficulty,
        questions=questions,
    )
