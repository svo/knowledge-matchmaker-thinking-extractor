from fastapi import APIRouter, HTTPException

from knowledge_matchmaker_thinking_extractor.application.use_case.extract_thinking_use_case import ExtractThinkingUseCase
from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.interface.api.data_transfer_object.extract_data_transfer_object import (
    ExtractRequest,
    ExtractResponse,
)


def create_extract_controller(use_case: ExtractThinkingUseCase) -> APIRouter:
    router = APIRouter()

    @router.post("/extract", response_model=ExtractResponse)
    async def extract(request: ExtractRequest) -> ExtractResponse:
        try:
            draft = Draft(text=request.draft)
            result = use_case.execute(draft)
            return ExtractResponse(
                claims=result.claims,
                assumptions=result.assumptions,
                framings=result.framings,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    return router
