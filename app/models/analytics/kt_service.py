"""Simplified MRTKT/DKVMN-style knowledge tracing placeholder.

中文：MRTKT/DKVMN 风格的占位推理逻辑，输出下一题正确率与掌握度向量。
"""

from __future__ import annotations

from typing import Dict, List

from ...models import KTResponse, StudentInteraction


def _time_decay_adjustment(timestamp_seq: List[float]) -> float:
    if len(timestamp_seq) < 2:
        return 1.0
    gaps = [timestamp_seq[i] - timestamp_seq[i - 1] for i in range(1, len(timestamp_seq))]
    avg_gap = sum(max(g, 0.0) for g in gaps) / len(gaps)
    # 将时间间隔映射到 [0.7, 1.0] 的衰减系数
    return max(0.7, min(1.0, 1.0 - avg_gap * 0.01))


def run_inference_kt(interactions: List[StudentInteraction]) -> KTResponse:
    """输入学生交互序列，输出下一题正确概率和知识掌握状态。"""
    if not interactions:
        return KTResponse(next_question_correct_prob=0.5, mastery={"K1": 0.5})

    correct_seq = [it.correct for it in interactions]
    time_seq = [it.timestamp for it in interactions]
    accuracy = sum(correct_seq) / len(correct_seq)
    time_decay = _time_decay_adjustment(time_seq)

    base_prob = accuracy * 0.8 + 0.1
    prob_with_decay = max(0.05, min(0.95, base_prob * time_decay))

    # 生成一个简化的 3 维知识掌握字典
    mastery_vec = {
        "K1": round(prob_with_decay * 0.95, 3),
        "K2": round(prob_with_decay * 1.05 if accuracy > 0.6 else prob_with_decay * 0.9, 3),
        "K3": round(prob_with_decay, 3),
    }
    next_prob = max(0.05, min(0.95, prob_with_decay + 0.05 * (correct_seq[-1] - 0.5)))

    return KTResponse(
        next_question_correct_prob=round(next_prob, 3),
        mastery=mastery_vec,
    )
