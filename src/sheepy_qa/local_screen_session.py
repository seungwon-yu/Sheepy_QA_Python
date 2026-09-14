"""실제 창 캡처를 사전조건 상태 전이에 연결한다. 게임 파일은 변경하지 않는다."""
import time
from PIL import Image
from sheepy_qa.screen_preparation import ScreenObservation, ensureScreen
from sheepy_qa.screen_capture import captureWindowScreenshot
from sheepy_qa.window_state import findWindowByProcessNameFragments, focusWindow
from sheepy_qa.image_analysis import analyzeImage
from sheepy_qa.language_screen import analyzeLanguageSelectionScreen
from sheepy_qa.lobby_menu import analyzeLobbyMenu
from sheepy_qa.image_diff import compareImages
from sheepy_qa.gameplay_screen import classifyGameplayScreen
from sheepy_qa.keyboard_input import pressEnter


class LocalScreenSession:
    def __init__(self, writer, runDir):
        self.writer = writer
        self.runDir = runDir
        self.index = 0
        self.window = None
        self.lastImage = None
        self.lobbyImage = None
        self.gameplay = None
        self.captureSize = None

    def observe(self):
        self.window = findWindowByProcessNameFragments(["sheepyashortadventure"])
        if self.window is None or not self.window.isForeground:
            return ScreenObservation("UNKNOWN", False)
        image = captureWindowScreenshot(self.window, self.runDir / f"prepare-{self.index:03d}.png")
        self.index += 1
        self.lastImage = image
        with Image.open(image) as captured:
            size = captured.size
        if self.captureSize is None:
            self.captureSize = size
        elif size != self.captureSize:
            self.writer.writeJson(self.runDir, f"prepare-{self.index - 1:03d}.json", {
                "state": "SCREEN_SIZE_CHANGED", "expectedSize": self.captureSize,
                "actualSize": size, "image": image
            })
            raise ValueError(f"화면 크기 변경: {self.captureSize} -> {size}; 비교와 추가 입력 중단")
        screen = analyzeImage(image)
        language = analyzeLanguageSelectionScreen(image)
        lobby = analyzeLobbyMenu(image)
        if screen.isMostlyBlack:
            state = "BLACK"
        elif language.isLanguageSelectionLike:
            state = "LANGUAGE"
        elif lobby.continueVisible or lobby.startJourneyVisible:
            state = "LOBBY"
            self.lobbyImage = image
        elif self.lobbyImage is not None:
            self.gameplay = classifyGameplayScreen(screen, language, lobby, compareImages(self.lobbyImage, image))
            state = "GAMEPLAY" if self.gameplay.isGameplayScreenCandidate else "POST_LANGUAGE"
        else:
            state = "POST_LANGUAGE" if screen.uniqueSampledColorCount > 10 else "UNKNOWN"
        self.writer.writeJson(self.runDir, f"prepare-{self.index - 1:03d}.json", {
            "state": state, "window": self.window, "screen": screen, "language": language, "lobby": lobby
        })
        return ScreenObservation(state, True)

    def enter(self):
        current = findWindowByProcessNameFragments(["sheepyashortadventure"])
        if current is None or not current.isForeground:
            raise RuntimeError("입력 직전 Sheepy foreground 확인 실패")
        pressEnter()

    def prepare(self, target):
        window = findWindowByProcessNameFragments(["sheepyashortadventure"])
        if window is not None:
            focusWindow(window.handle)
            time.sleep(0.3)
        try:
            result = ensureScreen(target, self.observe, self.enter, timeoutSeconds=30)
        except Exception as error:
            from sheepy_qa.screen_preparation import PreparationResult
            result = PreparationResult(False, target, "UNKNOWN", f"관찰/입력 오류: {type(error).__name__}: {error}")
        self.writer.writeJson(self.runDir, "preparation.json", result)
        return result

    def input(self, action):
        current = findWindowByProcessNameFragments(["sheepyashortadventure"])
        if current is None or not current.isForeground:
            raise RuntimeError("입력 직전 Sheepy foreground 확인 실패")
        action()
