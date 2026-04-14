# Feature: Align POST /extract Contract with Canonical Spec

## Overview

The thinking-extractor's `POST /extract` endpoint currently deviates from the canonical API contract defined in the parent repository's `.specs/initial/SPEC.md`. The request field is named `text` instead of `draft`, and the response returns a flat `positions` array instead of separate `claims`, `assumptions`, and `framings` arrays. These deviations break the contract that downstream consumers (relationship-engine) depend on.

## Motivation

The canonical spec deliberately separates extracted thinking into three named categories — claims, assumptions, and framings — because these categories carry different epistemic weight. A claim is something the user asserts; an assumption is something they take for granted; a framing is the lens they see through. The relationship-engine classifies literature against each of these differently. Collapsing them into a single `positions` array with a type discriminator loses this structure at the API boundary.

The `draft` field name aligns with the domain concept (`Draft`) used throughout the system. The current `text` field is a weaker name that doesn't carry domain meaning.

## Acceptance Criteria

- [ ] Given a request to `POST /extract`, when the body contains `{ "draft": "..." }`, then the endpoint accepts it and extracts thinking.
- [ ] Given a request to `POST /extract`, when the body contains `{ "text": "..." }`, then the endpoint rejects it with a 422 validation error.
- [ ] Given a successful extraction, when the response is returned, then it contains `{ "claims": ["..."], "assumptions": ["..."], "framings": ["..."] }`.
- [ ] Given a successful extraction, when the response is returned, then no field named `positions` exists in the response body.
- [ ] Given a draft with no identifiable assumptions, when extracted, then the `assumptions` array is empty.
- [ ] Given existing unit and integration tests, when the contract changes are applied, then all tests pass under `tox`.

## Current State

### Request DTO (`extract_thinking_data_transfer_object.py`)

```python
class ExtractThinkingRequestDto(BaseModel):
    text: str  # Should be: draft
```

### Response DTO (`extract_thinking_data_transfer_object.py`)

```python
class PositionDto(BaseModel):
    text: str
    position_type: str

class ExtractThinkingResponseDto(BaseModel):
    positions: list[PositionDto]  # Should be: claims, assumptions, framings
```

### Target Contract (from `.specs/initial/SPEC.md`)

```json
Request:  { "draft": "string" }
Response: {
  "claims": ["string"],
  "assumptions": ["string"],
  "framings": ["string"]
}
```

## Domain Model Impact

The domain models (`Draft`, `ExtractedThinking`, `Position`, `PositionType`) are sound and do not need to change. The `ExtractedThinking` model internally holds a list of `Position` objects with `PositionType` discriminators — this is a good internal representation.

The change is at the **interface layer** only:
- `ExtractThinkingRequestDto`: rename `text` → `draft`
- `ExtractThinkingResponseDto`: replace `positions: list[PositionDto]` with `claims: list[str]`, `assumptions: list[str]`, `framings: list[str]`
- `ExtractThinkingResponseDto.from_domain_model()`: filter positions by type into the three arrays
- Controller: update `Draft(text=request.text)` → `Draft(text=request.draft)`

## Cross-Service Impact

The relationship-engine's `ThinkingExtractorHttpClient` currently sends `{"text": draft_text}` and reads `response.json()["positions"]`. After this change, it must send `{"draft": draft_text}` and read `claims`, `assumptions`, `framings` from the response. That work is tracked in the relationship-engine's own spec.

## Open Questions

None — the target contract is fully defined in the canonical spec.
