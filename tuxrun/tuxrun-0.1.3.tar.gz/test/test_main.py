import pytest
import yaml

import tuxrun.__main__
from tuxrun.__main__ import start, main


def touch(directory, name):
    f = directory / name
    f.touch()
    return f


@pytest.fixture
def device(tmp_path):
    return touch(tmp_path, "device.yaml")


@pytest.fixture
def job(tmp_path):
    return touch(tmp_path, "job.yaml")


@pytest.fixture
def tuxrun_args(monkeypatch, device, job):
    args = ["tuxrun", "--device", str(device), "--definition", str(job)]
    monkeypatch.setattr("sys.argv", args)
    return args


@pytest.fixture
def lava_run(mocker):
    Popen = mocker.patch("subprocess.Popen")
    proc = Popen.return_value
    proc.wait.return_value = 0
    proc.communicate.return_value = (mocker.MagicMock(), mocker.MagicMock())
    return proc


def test_start_calls_main(monkeypatch, mocker):
    monkeypatch.setattr(tuxrun.__main__, "__name__", "__main__")
    main = mocker.patch("tuxrun.__main__.main")
    with pytest.raises(SystemExit):
        start()
    main.assert_called()


def test_main_usage(capsys):
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code != 0
    _, err = capsys.readouterr()
    assert "usage: tuxrun" in err


def test_almost_real_run(tuxrun_args, lava_run, capsys):
    lava_run.stderr = [
        '- {"lvl": "info", "msg": "Hello, world", "dt": ""2021-04-08T18:42:25.139513"\n'
    ]
    exitcode = main()
    assert exitcode == 0
    stdout, _ = capsys.readouterr()
    assert "Hello, world" in stdout


def test_ignores_empty_line_from_lava_run_stdout(tuxrun_args, lava_run):
    lava_run.stderr = [
        '{"lvl": "info", "msg": "Hello, world", "dt": "2021-04-08T18:42:25.139513"}\n',
        "",
        '{"lvl": "info", "msg": "Hello, world", "dt": "2021-04-08T18:42:26.139513"}\n',
    ]
    exitcode = main()
    assert exitcode == 0


def test_ignores_empty_line_from_lava_run_logfile(tuxrun_args, lava_run, tmp_path):
    log = tmp_path / "log.yaml"
    tuxrun_args += ["--log", str(log)]
    lava_run.stderr = [
        '{"lvl": "info", "msg": "Hello, world", "dt": "2021-04-08T18:42:25.139513"}\n',
        "",
        '{"lvl": "info", "msg": "Hello, world", "dt": "2021-04-08T18:42:26.139513"}\n',
    ]
    exitcode = main()
    assert exitcode == 0
    logdata = yaml.safe_load(log.open())
    assert type(logdata[0]) is dict
    assert type(logdata[1]) is dict
