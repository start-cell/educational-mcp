"""Lightweight placeholder for deep cognitive diagnosis inference.

中文：深度认知诊断（DeepIRT）占位推理逻辑，与路由解耦，生成掌握度向量。
"""

from __future__ import annotations

from typing import Dict, List

from ...pydantic_models import Interaction, MasteryResponse


class _MockDeepIRTModel:
    """代替真实 DeepIRT 的简化版，仅用于演示接口集成。"""

    def predict(self, input_data: tuple[List[int], List[int], List[int]]) -> List[float]:
        _, _, correctness = input_data
        if not correctness:
            return [0.5, 0.5, 0.5]
        accuracy = sum(correctness) / len(correctness)
        # 生成 3 维“知识掌握”向量，略微扰动以模拟不同知识点
        return [
            max(0.05, min(0.95, accuracy * 0.9 + 0.1)),
            max(0.05, min(0.95, accuracy * 0.8 + 0.15)),
            max(0.05, min(0.95, accuracy * 1.0)),
        ]


deepirt_model = _MockDeepIRTModel()


def run_inference_cdm(interactions: List[Interaction]) -> MasteryResponse:
    """输入学生交互序列，输出知识点掌握情况概率。"""
    student_ids = [it.student_id for it in interactions]
    item_ids = [it.item_id for it in interactions]
    correctness = [it.correct for it in interactions]
    input_data = (student_ids, item_ids, correctness)
    mastery_probs = deepirt_model.predict(input_data)
    mastery_dict: Dict[str, float] = {
        f"K{idx+1}": float(prob) for idx, prob in enumerate(mastery_probs)
    }
    return MasteryResponse(mastery=mastery_dict, raw_vector=list(mastery_probs))
