from __future__ import annotations

from unittest.mock import Mock

import pytest
from assertpy import assert_that
from fastapi import FastAPI
from fastapi.testclient import TestClient

from knowledge_matchmaker_thinking_extractor.application.use_case.extract_thinking_use_case import (
    ExtractThinkingUseCase,
)
from knowledge_matchmaker_thinking_extractor.domain.model.draft import Draft
from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking
from knowledge_matchmaker_thinking_extractor.domain.model.position import Position, PositionType
from knowledge_matchmaker_thinking_extractor.interface.api.controller.extract_thinking_controller import (
    ExtractThinkingController,
)


class TestExtractThinkingController:
    @pytest.fixture
    def mock_use_case(self) -> Mock:
        return Mock(spec=ExtractThinkingUseCase)

    @pytest.fixture
    def controller(self, mock_use_case: Mock) -> ExtractThinkingController:
        return ExtractThinkingController(extract_thinking_use_case=mock_use_case)

    @pytest.fixture
    def app(self, controller: ExtractThinkingController) -> FastAPI:
        application = FastAPI()
        application.include_router(controller.router)
        return application

    @pytest.fixture
    def client(self, app: FastAPI) -> TestClient:
        return TestClient(app)

    @pytest.fixture
    def extracted_thinking(self) -> ExtractedThinking:
        return ExtractedThinking(positions=[Position(text="a claim", position_type=PositionType.CLAIM)])

    def test_should_return_200_when_extract_is_called(
        self, client: TestClient, mock_use_case: Mock, extracted_thinking: ExtractedThinking
    ) -> None:
        mock_use_case.execute.return_value = extracted_thinking

        response = client.post("/extract", json={"text": "some draft text"})

        assert_that(response.status_code).is_equal_to(200)

    def test_should_return_positions_in_response(
        self, client: TestClient, mock_use_case: Mock, extracted_thinking: ExtractedThinking
    ) -> None:
        mock_use_case.execute.return_value = extracted_thinking

        response = client.post("/extract", json={"text": "some draft text"})

        assert_that(response.json()["positions"]).is_length(1)

    def test_should_call_use_case_with_draft_text(
        self, client: TestClient, mock_use_case: Mock, extracted_thinking: ExtractedThinking
    ) -> None:
        mock_use_case.execute.return_value = extracted_thinking

        client.post("/extract", json={"text": "some draft text"})

        mock_use_case.execute.assert_called_once_with(Draft(text="some draft text"))
