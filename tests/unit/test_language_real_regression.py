from pathlib import Path
from sheepy_qa.language_screen import analyzeLanguageSelectionScreen

def test_gameplay_image_is_not_language_selection():
    # 실제 오탐 장면의 회귀 검증이며 전체 인식 정확도 평가는 아니다.
    image = Path(__file__).resolve().parents[2] / "docs/samples/gameplay-language-false-positive.png"
    result = analyzeLanguageSelectionScreen(image)
    assert result.isLanguageSelectionLike is False
    # 이 오탐은 screen_preparation의 별도 회귀에서 추가 입력을 차단한다.
