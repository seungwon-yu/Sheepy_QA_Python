from sheepy_qa.process_check import ProcessSnapshot, hasRunningProcess


def test_has_running_process_returns_true_when_pid_exists() -> None:
    processes = [
        ProcessSnapshot(name="Sheepy.exe", pid=1234, status="running")
    ]

    assert hasRunningProcess(processes) is True


def test_has_running_process_returns_false_without_pid() -> None:
    processes = [
        ProcessSnapshot(name="Sheepy.exe", pid=0, status=None)
    ]

    assert hasRunningProcess(processes) is False
