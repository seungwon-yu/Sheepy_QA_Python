from sheepy_qa.wait import waitUntil


def test_wait_until_returns_immediately_when_predicate_matches() -> None:
    matched, value = waitUntil(
        supplier=lambda: "ready",
        predicate=lambda nextValue: nextValue == "ready",
        timeoutSeconds=0.1,
        intervalSeconds=0.01
    )

    assert matched is True
    assert value == "ready"


def test_wait_until_returns_last_value_when_timeout_expires() -> None:
    matched, value = waitUntil(
        supplier=lambda: "waiting",
        predicate=lambda nextValue: nextValue == "ready",
        timeoutSeconds=0.01,
        intervalSeconds=0.01
    )

    assert matched is False
    assert value == "waiting"
