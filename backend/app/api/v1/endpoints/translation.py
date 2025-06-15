import logging

from fastapi import APIRouter, HTTPException

from app.schemas.glossary_translation import (
    GlossaryBatchTranslationRequest,
    GlossaryBatchTranslationResponse,
    GlossaryTranslationRequest,
    GlossaryTranslationResponse,
    VerificationResults,
)
from app.schemas.translation import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    TranslationRequest,
    TranslationResponse,
)
from app.schemas.translation_evaluation import (
    TranslationEvaluationRequest,
    TranslationEvaluationResponse,
)
from app.services import glossary_aware_translation_service
from app.services.gemini_service import gemini_service
from app.services.translation_evaluation_service import translation_evaluation_service

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translate text using Google Gemini API.

    Args:
        request: Translation request containing source text and language codes

    Returns:
        Translation response with translated text
    """
    translated_text = await gemini_service.translate_text(
        source_text=request.source_text,
        source_lang=request.source_lang,
        target_lang=request.target_lang,
    )

    return TranslationResponse(
        translated_text=translated_text,
        source_text=request.source_text,
        source_lang=request.source_lang,
        target_lang=request.target_lang,
    )


@router.post("/translate/batch", response_model=BatchTranslationResponse)
async def translate_batch(request: BatchTranslationRequest):
    """
    Translate multiple texts using Google Gemini API.

    Args:
        request: Batch translation request containing list of texts and language codes

    Returns:
        Batch translation response with all translations
    """
    translations = []

    for text in request.texts:
        try:
            translated_text = await gemini_service.translate_text(
                source_text=text,
                source_lang=request.source_lang,
                target_lang=request.target_lang,
            )

            translations.append(
                TranslationResponse(
                    translated_text=translated_text,
                    source_text=text,
                    source_lang=request.source_lang,
                    target_lang=request.target_lang,
                )
            )
        except Exception as e:
            # For batch operations, we might want to continue with other translations
            # or handle errors differently based on requirements
            raise HTTPException(
                status_code=500,
                detail=f"Failed to translate text: {text[:50]}... Error: {e!s}",
            )

    return BatchTranslationResponse(translations=translations)


@router.post("/translate/glossary", response_model=GlossaryTranslationResponse)
async def translate_with_glossary(request: GlossaryTranslationRequest):
    """
    Translate text using glossary-aware translation.

    This endpoint wraps glossary terms before translation and verifies them after,
    ensuring consistent terminology.

    Args:
        request: Glossary translation request

    Returns:
        Glossary translation response with verification results
    """
    try:
        logger.info("=== STARTING GLOSSARY TRANSLATION ===")
        logger.info(
            f"Request: source_text='{request.source_text}', source_lang='{request.source_lang}', target_lang='{request.target_lang}', project_id='{request.project_id}'"
        )
        logger.info(
            f"Settings: preserve_forbidden_terms={request.preserve_forbidden_terms}, translate_allowed_terms={request.translate_allowed_terms}"
        )

        result = await glossary_aware_translation_service.translate_with_glossary(
            source_text=request.source_text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            project_id=request.project_id,
            preserve_forbidden_terms=request.preserve_forbidden_terms,
            translate_allowed_terms=request.translate_allowed_terms,
        )

        logger.info(f"Translation service returned: {list(result.keys())}")
        logger.info(f"Translated text length: {len(result['translated_text'])}")
        logger.info(f"Found {len(result['glossary_terms_found'])} glossary terms")

        response = GlossaryTranslationResponse(
            translated_text=result["translated_text"],
            source_text=result["source_text"],
            source_lang=result["source_lang"],
            target_lang=result["target_lang"],
            glossary_terms_found=result["glossary_terms_found"],
            wrapped_text=result["wrapped_text"],
            verification_results=VerificationResults(**result["verification_results"]),
        )

        logger.info("=== GLOSSARY TRANSLATION COMPLETED SUCCESSFULLY ===")
        return response

    except Exception as e:
        logger.error("=== GLOSSARY TRANSLATION FAILED ===")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {e!s}")
        logger.error("Full error details:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to translate with glossary: {e!s}",
        )


@router.post(
    "/translate/glossary/batch", response_model=GlossaryBatchTranslationResponse
)
async def translate_batch_with_glossary(request: GlossaryBatchTranslationRequest):
    """
    Translate multiple texts using glossary-aware translation.

    This endpoint processes multiple texts with glossary term protection.

    Args:
        request: Glossary batch translation request

    Returns:
        Glossary batch translation response with all translations
    """
    translations = []

    for text in request.texts:
        try:
            result = await glossary_aware_translation_service.translate_with_glossary(
                source_text=text,
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                project_id=request.project_id,
                preserve_forbidden_terms=request.preserve_forbidden_terms,
                translate_allowed_terms=request.translate_allowed_terms,
            )

            translations.append(
                GlossaryTranslationResponse(
                    translated_text=result["translated_text"],
                    source_text=result["source_text"],
                    source_lang=result["source_lang"],
                    target_lang=result["target_lang"],
                    glossary_terms_found=result["glossary_terms_found"],
                    wrapped_text=result["wrapped_text"],
                    verification_results=VerificationResults(
                        **result["verification_results"]
                    ),
                )
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to translate text with glossary: {text[:50]}... Error: {e!s}",
            )

    return GlossaryBatchTranslationResponse(translations=translations)


@router.get("/languages")
async def get_supported_languages():
    """
    Get list of supported language codes.

    Returns:
        Dictionary of supported language codes and their names
    """
    return {"languages": gemini_service.get_supported_languages()}


@router.post("/evaluate", response_model=TranslationEvaluationResponse)
async def evaluate_translation(request: TranslationEvaluationRequest):
    """
    Evaluate translation quality using objective metrics.

    This endpoint computes BLEU, TER, chrF scores and other metrics
    to assess translation quality against a reference translation.

    Args:
        request: Translation evaluation request

    Returns:
        Translation evaluation response with metric scores and assessment
    """
    try:
        logger.info("=== STARTING TRANSLATION EVALUATION ===")
        logger.info(
            f"Request: source='{request.source_text}' ({request.source_lang}), "
            f"translation='{request.translated_text}' ({request.target_lang}), "
            f"reference='{request.reference_text}', project_id='{request.project_id}'"
        )

        result = await translation_evaluation_service.evaluate_translation(
            source_text=request.source_text,
            source_lang=request.source_lang,
            translated_text=request.translated_text,
            target_lang=request.target_lang,
            reference_text=request.reference_text,
            project_id=request.project_id,
        )

        response = TranslationEvaluationResponse(**result)

        logger.info("=== TRANSLATION EVALUATION COMPLETED SUCCESSFULLY ===")
        return response

    except Exception as e:
        logger.error("=== TRANSLATION EVALUATION FAILED ===")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {e!s}")
        logger.error("Full error details:", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to evaluate translation: {e!s}",
        )
