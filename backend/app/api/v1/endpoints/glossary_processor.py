# # Save uploaded file temporarily
# import os
# import tempfile

# from fastapi import APIRouter, File, HTTPException, Query, UploadFile

# from app.schemas.glossary_processor import (
#     FoundTerm,
#     GlossaryLoadResponse,
#     GlossaryStats,
#     TermLookupRequest,
#     TermLookupResponse,
#     TextProcessingRequest,
#     TextProcessingResponse,
# )
# from app.services.glossary_processor import glossary_processor

# router = APIRouter()

# # Module-level variables for FastAPI parameter defaults
# REQUIRED_FILE = File(...)
# REQUIRED_PROJECT_ID = Query(..., description="Lokalise project ID")
# SOURCE_LANGUAGE = Query("en", description="Source language for terms")


# @router.post("/load", response_model=GlossaryLoadResponse)
# async def load_glossary_file(
#     file: UploadFile = REQUIRED_FILE,
#     project_id: str = REQUIRED_PROJECT_ID,
#     source_language: str = SOURCE_LANGUAGE,
# ):
#     """
#     Load glossary from an uploaded XLSX file and upload to Lokalise.

#     Args:
#         file: XLSX file containing glossary data
#         project_id: Lokalise project ID
#         source_language: Source language for terms (default: "en")

#     Returns:
#         Load response with success status and statistics
#     """
#     # Validate file type
#     if not file.filename or not file.filename.endswith((".xlsx", ".xls")):
#         raise HTTPException(
#             status_code=400, detail="Invalid file type. Please upload an XLSX file."
#         )

#     try:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
#             content = await file.read()
#             temp_file.write(content)
#             temp_file_path = temp_file.name

#         try:
#             # Load glossary from the temporary file and upload to Lokalise
#             await glossary_processor.load_glossary_from_xlsx(
#                 temp_file_path, project_id, source_language
#             )

#             # Get statistics
#             stats = await glossary_processor.get_stats(project_id)

#             return GlossaryLoadResponse(
#                 success=True,
#                 message=f"Successfully loaded and uploaded terms from {file.filename} to Lokalise project {project_id}",
#                 stats=GlossaryStats(**stats),
#             )
#         finally:
#             # Clean up temporary file
#             if os.path.exists(temp_file_path):
#                 os.unlink(temp_file_path)

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Failed to process glossary file: {e!s}"
#         ) from e


# @router.post("/find-terms", response_model=list[FoundTerm])
# async def find_terms(
#     request: TextProcessingRequest,
#     project_id: str = Query(..., description="Lokalise project ID"),
# ):
#     """
#     Find glossary terms in the provided text using Lokalise data.

#     Args:
#         request: Text processing request
#         project_id: Lokalise project ID

#     Returns:
#         List of found terms with their positions and metadata
#     """
#     try:
#         found_terms = await glossary_processor.find_terms_in_text(
#             request.text, project_id
#         )
#         return [FoundTerm(**term) for term in found_terms]
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Failed to find terms in text: {e!s}"
#         ) from e


# @router.post("/replace-terms", response_model=TextProcessingResponse)
# async def replace_terms(
#     request: TextProcessingRequest,
#     project_id: str = Query(..., description="Lokalise project ID"),
# ):
#     """
#     Replace glossary terms in text with their translations using Lokalise data.

#     Args:
#         request: Text processing request with target language
#         project_id: Lokalise project ID

#     Returns:
#         Text processing response with replaced text and found terms
#     """
#     if not request.target_lang:
#         raise HTTPException(
#             status_code=400, detail="Target language is required for term replacement"
#         )

#     try:
#         # Find terms first
#         found_terms = await glossary_processor.find_terms_in_text(
#             request.text, project_id
#         )

#         # Replace terms
#         processed_text = await glossary_processor.replace_terms_in_text(
#             request.text, request.target_lang, project_id
#         )

#         return TextProcessingResponse(
#             original_text=request.text,
#             processed_text=processed_text,
#             found_terms=[FoundTerm(**term) for term in found_terms],
#             target_lang=request.target_lang,
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Failed to replace terms in text: {e!s}"
#         ) from e


# @router.post("/wrap-terms", response_model=TextProcessingResponse)
# async def wrap_terms(
#     request: TextProcessingRequest,
#     project_id: str = Query(..., description="Lokalise project ID"),
# ):
#     """
#     Wrap glossary terms in text with protective tags for LLM input using Lokalise data.

#     Args:
#         request: Text processing request with wrapper tag
#         project_id: Lokalise project ID

#     Returns:
#         Text processing response with wrapped text and found terms
#     """
#     try:
#         # Find terms first
#         found_terms = await glossary_processor.find_terms_in_text(
#             request.text, project_id
#         )

#         # Wrap terms
#         processed_text = await glossary_processor.wrap_terms_in_text(
#             request.text, project_id, request.wrapper_tag
#         )

#         return TextProcessingResponse(
#             original_text=request.text,
#             processed_text=processed_text,
#             found_terms=[FoundTerm(**term) for term in found_terms],
#             target_lang=None,
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Failed to wrap terms in text: {e!s}"
#         ) from e


# @router.post("/lookup-term", response_model=TermLookupResponse)
# async def lookup_term(
#     request: TermLookupRequest,
#     project_id: str = Query(..., description="Lokalise project ID"),
# ):
#     """
#     Look up information for a specific term from Lokalise.

#     Args:
#         request: Term lookup request
#         project_id: Lokalise project ID

#     Returns:
#         Term lookup response with term information
#     """
#     try:
#         term_info = await glossary_processor.get_term_info(request.term, project_id)

#         if term_info is None:
#             return TermLookupResponse(
#                 term=request.term,
#                 found=False,
#                 translations=None,
#                 case_sensitive=None,
#                 forbidden=None,
#                 translatable=None,
#                 description=None,
#                 part_of_speech=None,
#                 tags=None,
#             )

#         return TermLookupResponse(
#             term=request.term,
#             found=True,
#             translations=term_info.get("translations"),
#             case_sensitive=term_info.get("case_sensitive"),
#             forbidden=term_info.get("forbidden"),
#             translatable=term_info.get("translatable"),
#             description=term_info.get("description"),
#             part_of_speech=term_info.get("part_of_speech"),
#             tags=term_info.get("tags"),
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Failed to lookup term: {e!s}"
#         ) from e


# @router.get("/languages", response_model=list[str])
# async def get_available_languages(
#     project_id: str = Query(..., description="Lokalise project ID"),
# ):
#     """
#     Get list of available languages in the glossary from Lokalise.

#     Args:
#         project_id: Lokalise project ID

#     Returns:
#         List of available language codes
#     """
#     try:
#         languages = await glossary_processor.get_available_languages(project_id)
#         return languages
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Failed to get available languages: {e!s}"
#         ) from e


# @router.get("/stats", response_model=GlossaryStats)
# async def get_glossary_stats(
#     project_id: str = Query(..., description="Lokalise project ID"),
# ):
#     """
#     Get glossary statistics from Lokalise.

#     Args:
#         project_id: Lokalise project ID

#     Returns:
#         Glossary statistics including term counts and available languages
#     """
#     try:
#         stats = await glossary_processor.get_stats(project_id)
#         return GlossaryStats(**stats)
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Failed to get glossary stats: {e!s}"
#         ) from e
