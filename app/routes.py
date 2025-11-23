"""FastAPI routes exposing educational mini-model endpoints.

中文：集中声明所有 HTTP 路由，把各小模型的输入输出暴露为接口。
不包含业务逻辑，具体处理委托给 services 层。"""

from __future__ import annotations

from fastapi import FastAPI

from .pydantic_models import (
    AffectiveAnalysisRequest,
    AffectiveAnalysisResponse,
    AspectSentimentRequest,
    AspectSentimentResponse,
    CognitiveDiagnosisRequest,
    CognitiveDiagnosisResponse,
    GradeAnswerRequest,
    GradeAnswerResponse,
    Interaction,
    IntensityRequest,
    IntensityResponse,
    KnowledgeTracingRequest,
    KnowledgeTracingResponse,
    KTResponse,
    MasteryResponse,
    PathRequest,
    PathResponse,
    SentimentRequest,
    SentimentResponse,
    PracticePlanRequest,
    PracticePlanResponse,
    ReflectionRequest,
    ReflectionResponse,
    StudentInteraction,
)
from .models import (
    analyze_affective_state,
    plan_learning_path,
    run_inference_aspect_sentiment,
    run_inference_cdm,
    run_inference_intensity,
    run_inference_kt,
    run_inference_sentiment,
    build_practice_plan,
    diagnose_cognition,
    generate_reflections,
    score_answer,
    trace_knowledge,
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Educational Mini-Models API",
        version="0.1.0",
        description="通过 FastAPI 暴露几个教育小模型示例接口。",
    )

    @app.post(
        "/grade-answer",
        response_model=GradeAnswerResponse,
        summary="主观题评分引擎",
        tags=["mini-models"],
        name="grade_answer",
    )
    def grade_answer(payload: GradeAnswerRequest) -> GradeAnswerResponse:
        """根据关键词覆盖率对学生作答进行简单打分。"""
        return score_answer(payload)

    @app.post(
        "/practice-plan",
        response_model=PracticePlanResponse,
        summary="生成个性化练习计划",
        tags=["mini-models"],
        name="practice_plan",
    )
    def practice_plan(payload: PracticePlanRequest) -> PracticePlanResponse:
        """根据学生薄弱点输出三阶段练习流程。"""
        return build_practice_plan(payload)

    @app.post(
        "/reflection-questions",
        response_model=ReflectionResponse,
        summary="课后反思问题生成",
        tags=["mini-models"],
        name="reflection_questions",
    )
    def reflection_questions(payload: ReflectionRequest) -> ReflectionResponse:
        """生成不同深度的课后反思问题，培养元认知能力。"""
        return generate_reflections(payload)

    @app.post(
        "/cognitive-diagnosis",
        response_model=CognitiveDiagnosisResponse,
        summary="认知诊断分析",
        tags=["mini-models", "learning-analytics"],
        name="cognitive_diagnosis",
    )
    def cognitive_diagnosis(payload: CognitiveDiagnosisRequest) -> CognitiveDiagnosisResponse:
        """根据概念掌握情况输出认知诊断和策略建议。"""
        return diagnose_cognition(payload)

    @app.post(
        "/knowledge-tracing",
        response_model=KnowledgeTracingResponse,
        summary="知识追踪预测",
        tags=["mini-models", "learning-analytics"],
        name="knowledge_tracing",
    )
    def knowledge_tracing(payload: KnowledgeTracingRequest) -> KnowledgeTracingResponse:
        """对学生的作答序列进行简单的知识追踪估计。"""
        return trace_knowledge(payload)

    @app.post(
        "/affective-analysis",
        response_model=AffectiveAnalysisResponse,
        summary="情感状态识别",
        tags=["mini-models", "affective-computing"],
        name="affective_analysis",
    )
    def affective_analysis(payload: AffectiveAnalysisRequest) -> AffectiveAnalysisResponse:
        """融合多模态情感信号，返回调控建议。"""
        return analyze_affective_state(payload)

    @app.post(
        "/cdm/mastery",
        response_model=MasteryResponse,
        summary="深度认知诊断（DeepIRT 推理）",
        tags=["learning-analytics"],
        name="get_mastery",
    )
    def get_mastery(interactions: list[Interaction]) -> MasteryResponse:
        """输入学生交互列表，输出知识点掌握概率向量。"""
        return run_inference_cdm(interactions)

    @app.post(
        "/kt/predict",
        response_model=KTResponse,
        summary="MRTKT 知识追踪预测",
        tags=["learning-analytics"],
        name="predict_next_and_mastery",
    )
    def predict_next_and_mastery(interactions: list[StudentInteraction]) -> KTResponse:
        """根据作答序列预测下一题正确率并给出当前知识掌握程度。"""
        return run_inference_kt(interactions)

    @app.post(
        "/path/recommend",
        response_model=PathResponse,
        summary="个性化学习路径规划",
        tags=["learning-path"],
        name="recommend_path",
    )
    def recommend_path(payload: PathRequest) -> PathResponse:
        """基于掌握度和先修图推荐下一步学习路径。"""
        return plan_learning_path(payload.mastery, payload.threshold, payload.max_recommend)

    @app.post(
        "/sentiment/analyze",
        response_model=SentimentResponse,
        summary="情感分类（BiLSTM+Attention 接口形态）",
        tags=["affective-computing"],
        name="analyze_sentiment",
    )
    def analyze_sentiment(payload: SentimentRequest) -> SentimentResponse:
        """返回文本的正/中/负情感概率与标签。"""
        return run_inference_sentiment(payload.text)

    @app.post(
        "/sentiment/aspect",
        response_model=AspectSentimentResponse,
        summary="方面级情感分析（BERT+Aspect Embedding 接口形态）",
        tags=["affective-computing"],
        name="analyze_aspect_sentiment",
    )
    def analyze_aspect_sentiment(payload: AspectSentimentRequest) -> AspectSentimentResponse:
        """对指定方面返回情感标签。"""
        return run_inference_aspect_sentiment(payload.text, payload.aspects)

    @app.post(
        "/sentiment/intensity",
        response_model=IntensityResponse,
        summary="情感强度回归（RoBERTa 接口形态）",
        tags=["affective-computing"],
        name="analyze_intensity",
    )
    def analyze_intensity(payload: IntensityRequest) -> IntensityResponse:
        """给出文本情感强度 0-1 分值。"""
        return run_inference_intensity(payload.text)

    return app
