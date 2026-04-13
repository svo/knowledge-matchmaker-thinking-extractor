from typing import Any, Dict


class SharedStorage:
    def __init__(self) -> None:
        self._storage: Dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self._storage.get(key)

    def set(self, key: str, value: Any) -> None:
        self._storage[key] = value
