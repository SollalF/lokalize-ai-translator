from typing import Any

from pydantic import BaseModel, Field


class TranslationEvaluationRequest(BaseModel):
    """Request model for translation evaluation."""

    source_text: str = Field(..., description="Original text to be translated")
    source_lang: str = Field(
        ..., max_length=10, description="Source language code (e.g., 'en', 'es_419')"
    )
    translated_text: str = Field(..., description="The translated text to evaluate")
    target_lang: str = Field(
        ..., max_length=10, description="Target language code (e.g., 'en', 'es_419')"
    )
    reference_text: str | None = Field(
        None, description="Optional reference translation for comparison"
    )
    project_id: str | None = Field(
        None, description="Optional Lokalise project ID for glossary checking"
    )


class MetricScores(BaseModel):
    """Model for objective translation metrics."""

    bleu: float | None = Field(None, description="BLEU score (0-100, higher is better)")
    ter: float | None = Field(
        None, description="Translation Error Rate (0-100, lower is better)"
    )
    chrf: float | None = Field(None, description="chrF score (0-100, higher is better)")
    edit_distance: int | None = Field(
        None, description="Character-level edit distance (lower is better)"
    )


class GlossaryCompliance(BaseModel):
    """Model for glossary compliance checking results."""

    terms_found_in_source: list[dict[str, Any]] = Field(
        default_factory=list, description="Glossary terms found in source text"
    )
    terms_correctly_handled: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Terms that were correctly preserved/translated",
    )
    terms_incorrectly_handled: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Terms that were not handled according to glossary rules",
    )
    compliance_score: float | None = Field(
        None, description="Percentage of terms correctly handled (0-100)"
    )
    compliance_summary: str = Field(..., description="Summary of glossary compliance")


class LLMFeedback(BaseModel):
    """Model for LLM qualitative feedback on translation."""

    strengths: list[str] = Field(
        default_factory=list, description="Positive aspects of the translation"
    )
    weaknesses: list[str] = Field(
        default_factory=list, description="Areas for improvement in the translation"
    )
    specific_comments: list[dict[str, str]] = Field(
        default_factory=list,
        description="Specific comments about parts of the translation",
    )
    suggestions: list[str] = Field(
        default_factory=list, description="Specific improvement suggestions"
    )
    summary: str = Field(..., description="Overall qualitative assessment summary")


class TranslationEvaluationResponse(BaseModel):
    """Response model for translation evaluation."""

    source_text: str = Field(..., description="Original source text")
    translated_text: str = Field(..., description="The translated text")
    reference_text: str | None = Field(None, description="Reference text if provided")
    source_lang: str = Field(..., description="Source language code")
    target_lang: str = Field(..., description="Target language code")
    metric_scores: MetricScores = Field(..., description="Objective metric scores")
    glossary_compliance: GlossaryCompliance | None = Field(
        None, description="Glossary compliance results (if project_id provided)"
    )
    llm_feedback: LLMFeedback | None = Field(
        None, description="LLM qualitative feedback on translation quality"
    )
    overall_assessment: str = Field(
        ...,
        description="Overall quality assessment (based on metrics if reference provided, otherwise descriptive)",
    )
