from pathlib import Path
import pytest
from sheepy_qa.language_screen import analyzeLanguageSelectionScreen

@pytest.mark.xfail(strict=True, reason="실제 플레이 화면의 언어 후보 오탐: 미해결")
def test_gameplay_image_is_not_language_selection():
    # 알려진 미해결 한계를 고정한 재현 테스트. 정상 인식 정확도 통과가 아니다.
    image = Path(__file__).resolve().parents[2] / "docs/samples/gameplay-language-false-positive.png"
    result = analyzeLanguageSelectionScreen(image)
    assert result.isLanguageSelectionLike is False
    # 이 오탐은 screen_preparation의 별도 회귀에서 추가 입력을 차단한다.
