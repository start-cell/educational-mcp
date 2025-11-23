"""Personalized learning path planning helper.

中文：学习路径规划业务逻辑，基于先修图和掌握度阈值推荐下一步知识点。
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List

from ...pydantic_models import PathResponse

# 示例先修图，可替换为数据库或配置加载
adjacency_list: Dict[str, List[str]] = {
    "K1": ["K2", "K3"],
    "K2": ["K4"],
    "K3": ["K4", "K5"],
    "K4": [],
    "K5": [],
}


def plan_learning_path(mastery: Dict[str, float], threshold: float, max_recommend: int) -> PathResponse:
    """基于拓扑排序 + 掌握度筛选规划学习路径。"""
    indegree: Dict[str, int] = {k: 0 for k in adjacency_list}
    for prereq, next_list in adjacency_list.items():
        for nxt in next_list:
            indegree[nxt] = indegree.get(nxt, 0) + 1

    queue = deque([k for k, deg in indegree.items() if deg == 0])
    recommended: List[str] = []
    visited = set()

    while queue and len(recommended) < max_recommend:
        cur = queue.popleft()
        visited.add(cur)

        if mastery.get(cur, 0.0) < threshold:
            recommended.append(cur)
            if len(recommended) >= max_recommend:
                break

        for nxt in adjacency_list.get(cur, []):
            indegree[nxt] -= 1
            if indegree[nxt] == 0 and nxt not in visited:
                queue.append(nxt)

    return PathResponse(recommended_path=recommended)
