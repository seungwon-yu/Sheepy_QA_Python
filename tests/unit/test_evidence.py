import json

from sheepy_qa.evidence import EvidenceWriter, sanitizeFileName


def test_sanitize_file_name_replaces_unsafe_characters() -> None:
    assert sanitizeFileName("TC-002 Sheepy AppID 실행 시도") == "TC-002_Sheepy_AppID_실행_시도"


def test_evidence_writer_creates_json_file(tmp_path) -> None:
    writer = EvidenceWriter(baseDir=tmp_path)
    runDir = writer.createRunDir("TC-001")
    filePath = writer.writeJson(runDir, "result.json", {"result": "PASS"})

    assert filePath.exists()
    assert json.loads(filePath.read_text(encoding="utf-8")) == {"result": "PASS"}
