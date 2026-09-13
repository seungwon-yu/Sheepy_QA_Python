"""지원하는 화면 전환만 수행하는 제한된 사전조건 준비."""
from dataclasses import dataclass, field
from time import monotonic, sleep
from typing import Callable


@dataclass(frozen=True)
class ScreenObservation:
    state: str
    foreground: bool = True


@dataclass
class PreparationResult:
    ready: bool
    target: str
    actual: str
    reason: str
    events: list[dict] = field(default_factory=list)


def ensureScreen(
    target: str,
    observe: Callable[[], ScreenObservation],
    enter: Callable[[], None],
    timeoutSeconds: float = 15,
    intervalSeconds: float = 0.5,
    clock: Callable[[], float] = monotonic,
    pause: Callable[[float], None] = sleep
) -> PreparationResult:
    if target not in {"POST_LANGUAGE", "LOBBY", "GAMEPLAY"}:
        raise ValueError("지원하지 않는 목표 화면")
    if timeoutSeconds <= 0 or intervalSeconds <= 0:
        raise ValueError("대기 시간은 양수여야 한다.")
    started = clock()
    events = []
    sentFrom = set()
    candidateSince = None
    loadingObserved = False
    while True:
        current = observe()
        events.append({"elapsed": round(clock() - started, 3), "state": current.state, "foreground": current.foreground})
        if not current.foreground:
            return PreparationResult(False, target, current.state, "대상 창 포커스 또는 캡처 조건 부족", events)
        if current.state == "LANGUAGE" and "LOBBY" in sentFrom:
            return PreparationResult(False, target, current.state, "로비 진입 후 예상하지 않은 언어 후보: 추가 입력 중단", events)
        accepted = {target} if target != "POST_LANGUAGE" else {"POST_LANGUAGE", "LOBBY", "GAMEPLAY"}
        if current.state == "BLACK" and "LOBBY" in sentFrom:
            loadingObserved = True
        if target == "GAMEPLAY":
            if current.state == "GAMEPLAY" and ("LOBBY" not in sentFrom or loadingObserved):
                if candidateSince is None:
                    candidateSince = clock()
            else:
                candidateSince = None
        sustained = target != "GAMEPLAY" or (candidateSince is not None and clock() - candidateSince >= 2)
        if current.state in accepted and sustained:
            return PreparationResult(True, target, current.state, "필요한 화면 관찰 조건 충족; 제품 전체 정상 판정은 아님", events)
        if current.state not in {"LANGUAGE", "BLACK", "LOBBY", "POST_LANGUAGE", "GAMEPLAY"}:
            return PreparationResult(False, target, current.state, "알 수 없는 화면에서 입력하지 않고 검토", events)
        elapsed = clock() - started
        if elapsed >= timeoutSeconds:
            return PreparationResult(False, target, current.state, "화면 준비 제한 시간 초과", events)
        canEnter = current.state == "LANGUAGE" or (current.state == "LOBBY" and target == "GAMEPLAY")
        if canEnter and current.state not in sentFrom:
            enter()
            sentFrom.add(current.state)
            events.append({"action": "ENTER", "from": current.state})
        pause(min(intervalSeconds, timeoutSeconds - elapsed))


def ensureLobbyScreen(observe, enter, **options):
    return ensureScreen("LOBBY", observe, enter, **options)


def ensureGameplayScreen(observe, enter, **options):
    return ensureScreen("GAMEPLAY", observe, enter, **options)
