import sys
import uvicorn
from fastapi import FastAPI
from lagom import Container

from knowledge_matchmaker_thinking_extractor.application.use_case.extract_thinking_use_case import ExtractThinkingUseCase
from knowledge_matchmaker_thinking_extractor.application.use_case.health_use_case import HealthUseCase
from knowledge_matchmaker_thinking_extractor.domain.health.health_checker import HealthChecker
from knowledge_matchmaker_thinking_extractor.domain.service.thinking_extractor import ThinkingExtractor
from knowledge_matchmaker_thinking_extractor.infrastructure.claude.claude_thinking_extractor import ClaudeThinkingExtractor
from knowledge_matchmaker_thinking_extractor.infrastructure.security.basic_authentication import (
    BasicAuthenticator,
    SecurityDependency,
    get_basic_authenticator,
)
from knowledge_matchmaker_thinking_extractor.infrastructure.system.health_factory import create_health_checker
from knowledge_matchmaker_thinking_extractor.interface.api.controller.extract_thinking_controller import (
    create_extract_thinking_controller,
)
from knowledge_matchmaker_thinking_extractor.interface.api.controller.health_controller import create_health_controller
from knowledge_matchmaker_thinking_extractor.shared.configuration import get_application_setting_provider

app = FastAPI(title="Knowledge Matchmaker Thinking Extractor API", version="1.0.0")


def get_container() -> Container:
    container = Container()

    claude_thinking_extractor = ClaudeThinkingExtractor()
    container[ThinkingExtractor] = lambda: claude_thinking_extractor  # type: ignore
    container[ExtractThinkingUseCase] = ExtractThinkingUseCase

    authenticator = get_basic_authenticator()
    security_dependency = SecurityDependency(authenticator)
    container[BasicAuthenticator] = lambda: authenticator
    container[SecurityDependency] = lambda: security_dependency

    health_checker = create_health_checker()
    container[HealthChecker] = lambda: health_checker  # type: ignore
    container[HealthUseCase] = HealthUseCase

    return container


global_container = get_container()


def get_global_container() -> Container:
    return global_container


security_dependency = global_container[SecurityDependency]
authentication_dependency = security_dependency.authentication_dependency()

extract_thinking_controller = create_extract_thinking_controller(global_container)
app.include_router(extract_thinking_controller.router)

health_use_case = global_container[HealthUseCase]
health_controller = create_health_controller(health_use_case)
app.include_router(health_controller)


def main(args: list) -> None:
    settings_provider = get_application_setting_provider()
    reload_setting = settings_provider.get("reload")
    host_setting = settings_provider.get("host")

    uvicorn.run(
        "knowledge_matchmaker_thinking_extractor.interface.api.main:app",
        reload=reload_setting,
        host=host_setting,
    )


def run() -> None:
    main(sys.argv[1:])
