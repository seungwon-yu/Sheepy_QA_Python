"""프로세스 감지의 시간별 근거. 실행 명령 성공이나 창 준비를 보장하지 않는다."""
import math
import time
from dataclasses import dataclass
from typing import Callable

from sheepy_qa.process_check import ProcessSnapshot, hasRunningProcess


@dataclass(frozen=True)
class ProcessObservation:
    detected: bool
    initialProcessPresent: bool
    elapsedSeconds: float
    samples: list[dict]


def observeProcessUntil(supplier: Callable[[], list[ProcessSnapshot]], timeoutSeconds=60,
                        intervalSeconds=1, clock=time.monotonic, sleep=time.sleep):
    if not math.isfinite(timeoutSeconds) or timeoutSeconds < 0:
        raise ValueError("timeoutSeconds must be finite and nonnegative")
    if not math.isfinite(intervalSeconds) or intervalSeconds <= 0:
        raise ValueError("intervalSeconds must be finite and positive")
    started = clock()
    samples = []
    while True:
        processes = supplier()
        elapsed = clock() - started
        detected = hasRunningProcess(processes)
        samples.append({"elapsedSeconds": round(elapsed, 6), "detected": detected,
                        "processes": processes})
        if detected or elapsed >= timeoutSeconds:
            return ProcessObservation(detected, samples[0]["detected"],
                                      round(elapsed, 6), samples)
        sleep(min(intervalSeconds, timeoutSeconds - elapsed))
