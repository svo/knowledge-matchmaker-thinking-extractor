from assertpy import assert_that

from knowledge_matchmaker_thinking_extractor.infrastructure.persistence.in_memory.shared_storage import (
    SharedStorage,
)


class TestSharedStorage:
    def test_should_return_none_when_key_does_not_exist(self):
        storage = SharedStorage()

        assert_that(storage.get("nonexistent")).is_none()

    def test_should_return_value_when_key_exists(self):
        storage = SharedStorage()
        storage.set("key", "value")

        assert_that(storage.get("key")).is_equal_to("value")

    def test_should_overwrite_existing_value(self):
        storage = SharedStorage()
        storage.set("key", "first")
        storage.set("key", "second")

        assert_that(storage.get("key")).is_equal_to("second")
