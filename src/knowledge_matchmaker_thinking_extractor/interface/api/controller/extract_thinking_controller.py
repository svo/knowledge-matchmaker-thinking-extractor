from __future__ import annotations

from fastapi import APIRouter

from lagom import Container

from knowledge_matchmaker_thinking_extractor.application.use_case.extract_thinking_use_case import ExtractThinkingUseCase
from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.interface.api.data_transfer_object.extract_thinking_data_transfer_object import (
    ExtractThinkingRequestDto,
    ExtractThinkingResponseDto,
)


class ExtractThinkingController:
    def __init__(self, extract_thinking_use_case: ExtractThinkingUseCase) -> None:
        self._extract_thinking_use_case = extract_thinking_use_case
        self.router = APIRouter(prefix="/extract", tags=["extract"])
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            "",
            self.extract,
            methods=["POST"],
            response_model=ExtractThinkingResponseDto,
        )

    async def extract(self, request: ExtractThinkingRequestDto) -> ExtractThinkingResponseDto:
        draft = Draft(text=request.text)
        extracted_thinking = self._extract_thinking_use_case.execute(draft)
        return ExtractThinkingResponseDto.from_domain_model(extracted_thinking)


def create_extract_thinking_controller(container: Container) -> ExtractThinkingController:
    extract_thinking_use_case = container[ExtractThinkingUseCase]
    return ExtractThinkingController(extract_thinking_use_case=extract_thinking_use_case)
