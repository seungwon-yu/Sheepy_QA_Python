"""로컬 pytest에서 준비 실패와 시각 반응 결과를 구분하는 지원 코드."""
import time
import pytest
from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.local_screen_session import LocalScreenSession
from sheepy_qa.local_test_config import shouldRunSteamTests
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord
from sheepy_qa.image_diff import compareImages
from sheepy_qa.image_evaluation import INPUT_RESPONSE_THRESHOLD
from sheepy_qa.screen_capture import captureWindowScreenshot

def prepareCheck(testId, target):
    if not shouldRunSteamTests():
        pytest.skip("NOT_RUN: SHEEPY_RUN_STEAM_TESTS=1이 필요한 실제 게임 테스트")
    writer = EvidenceWriter()
    runDir = writer.createRunDir(testId)
    session = LocalScreenSession(writer, runDir)
    prepared = session.prepare(target)
    if not prepared.ready:
        record = createJudgementRecord(target, prepared.actual, False, [], [], [
            JudgementCondition("화면 사전조건", target, prepared.actual, False, "preparation.json")
        ])
        writer.writeJson(runDir, "judgement.json", record)
        pytest.skip("REVIEW_REQUIRED: " + prepared.reason)
    return writer, runDir, session, prepared

def runVisualInputCheck(testId, action):
    writer, runDir, session, prepared = prepareCheck(testId, "GAMEPLAY")
    before = session.lastImage
    time.sleep(1)
    idleObservation = session.observe()
    if not idleObservation.foreground or idleObservation.state != "GAMEPLAY":
        record = createJudgementRecord("INPUT_VISUAL_RESPONSE", "REVIEW_REQUIRED", False, [], [])
        writer.writeJson(runDir, "judgement.json", record)
        pytest.skip("REVIEW_REQUIRED: 무입력 관찰 중 대상 창 또는 플레이 후보 상태 상실")
    idle = session.lastImage
    performed = False
    error = None
    try:
        # 복합 action도 각 키 직전에 대상 창을 다시 확인한다.
        action(session)
        performed = True
        time.sleep(1)
        observed = session.observe()
    except Exception as caught:
        error = str(caught)
        observed = None
    writer.writeJson(runDir, "input-log.json", {"actionPerformed": performed, "error": error})
    if observed is None or not observed.foreground or observed.state != "GAMEPLAY":
        record = createJudgementRecord("INPUT_VISUAL_RESPONSE", "REVIEW_REQUIRED", False, [], [])
        writer.writeJson(runDir, "judgement.json", record)
        pytest.skip("REVIEW_REQUIRED: 입력/관찰 조건 부족")
    idleDiff = compareImages(before, idle)
    inputDiff = compareImages(idle, session.lastImage)
    delta = round(inputDiff.changedPixelRatio - idleDiff.changedPixelRatio, 4)
    writer.writeJson(runDir, "idle-diff.json", idleDiff)
    writer.writeJson(runDir, "input-diff.json", inputDiff)
    writer.writeJson(runDir, "visual-response.json", {"delta": delta, "threshold": INPUT_RESPONSE_THRESHOLD, "scope": "시각적 반응이며 실제 이동/점프 성공 확정은 아님"})
    record = createJudgementRecord("INPUT_VISUAL_RESPONSE", "OBSERVED" if delta >= INPUT_RESPONSE_THRESHOLD else "NOT_CLEAR", performed,
        [JudgementCondition("무입력 대비 변화량", ">=0.005", delta, delta >= INPUT_RESPONSE_THRESHOLD, "visual-response.json")], [],
        [JudgementCondition("준비 완료", True, prepared.ready, prepared.ready, "preparation.json")])
    writer.writeJson(runDir, "judgement.json", record)
    assert record.result == "PASS", record.judgementBasis
