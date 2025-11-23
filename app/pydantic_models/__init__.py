"""Model schemas grouped by mini-model so FastAPI/MCP can import succinctly.

中文：集中导出各小模型的 Pydantic 数据模型，供路由与服务层引用。
"""

from .affective_state import (
    AffectiveAnalysisRequest,
    AffectiveAnalysisResponse,
    AffectiveSignal,
    AffectiveState,
)
from .cognitive_diagnosis import (
    CognitiveDiagnosisRequest,
    CognitiveDiagnosisResponse,
    ConceptDiagnosis,
    ConceptSnapshot,
)
from .grading import GradeAnswerRequest, GradeAnswerResponse
from .knowledge_tracing import (
    KTResponse,
    KnowledgeTracingRequest,
    KnowledgeTracingResponse,
    SkillInteraction,
    SkillProgress,
    StudentInteraction,
)
from .cdm import Interaction, MasteryResponse
from .path_planning import PathRequest, PathResponse
from .sentiment import SentimentRequest, SentimentResponse
from .aspect_sentiment import AspectSentimentRequest, AspectSentimentResponse
from .emotion_intensity import IntensityRequest, IntensityResponse
from .practice import PracticePhase, PracticePlanRequest, PracticePlanResponse
from .reflection import ReflectionRequest, ReflectionResponse

__all__ = [
    "AffectiveAnalysisRequest",
    "AffectiveAnalysisResponse",
    "AffectiveSignal",
    "AffectiveState",
    "CognitiveDiagnosisRequest",
    "CognitiveDiagnosisResponse",
    "ConceptDiagnosis",
    "ConceptSnapshot",
    "GradeAnswerRequest",
    "GradeAnswerResponse",
    "Interaction",
    "MasteryResponse",
    "KnowledgeTracingRequest",
    "KnowledgeTracingResponse",
    "SkillInteraction",
    "SkillProgress",
    "StudentInteraction",
    "KTResponse",
    "PathRequest",
    "PathResponse",
    "SentimentRequest",
    "SentimentResponse",
    "AspectSentimentRequest",
    "AspectSentimentResponse",
    "IntensityRequest",
    "IntensityResponse",
    "PracticePhase",
    "PracticePlanRequest",
    "PracticePlanResponse",
    "ReflectionRequest",
    "ReflectionResponse",
]
