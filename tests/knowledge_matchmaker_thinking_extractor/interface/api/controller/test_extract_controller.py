from unittest.mock import Mock

from assertpy import assert_that
from fastapi import FastAPI
from fastapi.testclient import TestClient

from knowledge_matchmaker_thinking_extractor.application.use_case.extract_thinking_use_case import ExtractThinkingUseCase
from knowledge_matchmaker_thinking_extractor.domain.model.extracted_thinking import ExtractedThinking
from knowledge_matchmaker_thinking_extractor.interface.api.controller.extract_controller import create_extract_controller


def _make_client(use_case: ExtractThinkingUseCase) -> TestClient:
    app = FastAPI()
    app.include_router(create_extract_controller(use_case))
    return TestClient(app)


class TestExtractController:
    def test_should_return_200_when_extract_succeeds(self) -> None:
        use_case = Mock(spec=ExtractThinkingUseCase)
        use_case.execute.return_value = ExtractedThinking(claims=[], assumptions=[], framings=[])
        client = _make_client(use_case)

        response = client.post("/extract", json={"draft": "some text"})

        assert_that(response.status_code).is_equal_to(200)

    def test_should_return_claims_when_extraction_produces_claims(self) -> None:
        use_case = Mock(spec=ExtractThinkingUseCase)
        use_case.execute.return_value = ExtractedThinking(claims=["my claim"], assumptions=[], framings=[])
        client = _make_client(use_case)

        response = client.post("/extract", json={"draft": "some text"})

        assert_that(response.json()["claims"]).contains("my claim")

    def test_should_return_assumptions_when_extraction_produces_assumptions(self) -> None:
        use_case = Mock(spec=ExtractThinkingUseCase)
        use_case.execute.return_value = ExtractedThinking(claims=[], assumptions=["my assumption"], framings=[])
        client = _make_client(use_case)

        response = client.post("/extract", json={"draft": "some text"})

        assert_that(response.json()["assumptions"]).contains("my assumption")

    def test_should_return_framings_when_extraction_produces_framings(self) -> None:
        use_case = Mock(spec=ExtractThinkingUseCase)
        use_case.execute.return_value = ExtractedThinking(claims=[], assumptions=[], framings=["my framing"])
        client = _make_client(use_case)

        response = client.post("/extract", json={"draft": "some text"})

        assert_that(response.json()["framings"]).contains("my framing")

    def test_should_return_500_when_use_case_raises_exception(self) -> None:
        use_case = Mock(spec=ExtractThinkingUseCase)
        use_case.execute.side_effect = Exception("some error")
        client = _make_client(use_case)

        response = client.post("/extract", json={"draft": "some text"})

        assert_that(response.status_code).is_equal_to(500)
