# Plan: Align POST /extract Contract with Canonical Spec

## Implementation Strategy

The change is confined to the interface layer — domain models and application logic remain unchanged. The `ExtractedThinking` domain model already holds `Position` objects with `PositionType` discriminators; the DTO's `from_domain_model()` method simply needs to filter by type into three separate arrays instead of returning a flat list.

All changes happen in the interface layer. No domain or application code changes.

## Changes

### Interface layer

**`interface/api/data_transfer_object/extract_thinking_data_transfer_object.py`**

Current:
```python
class ExtractThinkingRequestDto(BaseModel):
    text: str

class PositionDto(BaseModel):
    text: str
    position_type: str

class ExtractThinkingResponseDto(BaseModel):
    positions: list[PositionDto]
```

Target:
```python
class ExtractThinkingRequestDto(BaseModel):
    draft: str

class ExtractThinkingResponseDto(BaseModel):
    claims: list[str]
    assumptions: list[str]
    framings: list[str]
```

- Remove `PositionDto` (no longer needed — the response uses plain string arrays)
- Rename `ExtractThinkingRequestDto.text` → `ExtractThinkingRequestDto.draft`
- Replace `positions: list[PositionDto]` with `claims: list[str]`, `assumptions: list[str]`, `framings: list[str]`
- Update `from_domain_model()` to filter `extracted_thinking.positions` by `PositionType` into three lists, extracting the `.text` from each `Position`

**`interface/api/controller/extract_thinking_controller.py`**

- Update `Draft(text=request.text)` → `Draft(text=request.draft)`

### Tests

**`tests/.../interface/api/controller/test_extract_thinking_controller.py`**

- Update request payload in all tests: `{"text": "..."}` → `{"draft": "..."}`
- Update response assertions: check for `claims`, `assumptions`, `framings` arrays instead of `positions`
- Add tests asserting `positions` key is absent from response

**`tests/.../interface/api/data_transfer_object/test_extract_thinking_data_transfer_object.py`** (if exists, or add to controller tests)

- Test `from_domain_model()` correctly separates positions into three arrays by type
- Test empty positions produces three empty arrays
- Test positions of only one type produce correct distribution

## Task List

1. [ ] Update `ExtractThinkingRequestDto`: rename `text` → `draft`
2. [ ] Update `ExtractThinkingResponseDto`: replace `positions` with `claims`, `assumptions`, `framings`; update `from_domain_model()` to filter by `PositionType`
3. [ ] Remove `PositionDto` class (no longer used)
4. [ ] Update controller: `Draft(text=request.text)` → `Draft(text=request.draft)`
5. [ ] Update controller integration tests: request payload and response assertions
6. [ ] Add DTO unit tests for `from_domain_model()` filtering logic
7. [ ] Run `tox` to verify all tests pass with 100% coverage and all quality gates

## Testing Strategy

**Unit tests**: Test `ExtractThinkingResponseDto.from_domain_model()` with various combinations of position types to verify correct filtering into claims/assumptions/framings arrays.

**Integration tests**: Test `POST /extract` endpoint with the new request format (`{"draft": "..."}`) and verify the response structure matches `{ "claims": [...], "assumptions": [...], "framings": [...] }`.

**Negative test**: Verify that sending `{"text": "..."}` returns 422 validation error.

## Risks and Mitigations

- **Risk**: Relationship-engine breaks if it calls before updating its client. **Mitigation**: Both changes should be coordinated. The relationship-engine spec tracks the consumer-side update.
- **Risk**: `PositionDto` removal may leave orphan imports. **Mitigation**: `tox` (flake8) will catch unused imports.
