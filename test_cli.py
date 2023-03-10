from client_v2 import GET, PUT, POST, DELETE
from click.testing import CliRunner
from pathlib import Path


cli_runner = CliRunner()


def test_get_1():
    res = cli_runner.invoke(GET, [])
    assert res.exit_code == 0
    assert 'OK\n' in res.output


def test_get_2():
    res = cli_runner.invoke(GET, ['-p', '127.0.0.1:8001'])
    assert res.exit_code == 0
    assert 'OK\n' in res.output


def test_put_1():
    res = cli_runner.invoke(PUT, [f'{str(Path.cwd())}/client.py'])
    assert res.exit_code == 0
    assert 'OK\n' == res.output


def test_put_2():
    res = cli_runner.invoke(
        PUT, ['-p', '127.0.0.1:8001', f'{str(Path.cwd())}/client.py'])
    assert res.exit_code == 0
    assert 'OK\n' == res.output


def test_get_3():
    res = cli_runner.invoke(GET, [])
    assert res.exit_code == 0
    assert 'OK\n' in res.output


def test_get_4():
    res = cli_runner.invoke(GET, ['-p', '127.0.0.1:8001'])
    assert res.exit_code == 0
    assert 'OK\n' in res.output


def test_get_5():
    res = cli_runner.invoke(GET, ['client.py', str(
        Path.cwd())[:str(Path.cwd()).rfind('/')]])
    assert res.exit_code == 0
    assert 'OK\n' == res.output


def test_get_6():
    res = cli_runner.invoke(GET, ['-p', '127.0.0.1:8001', 'client.py', str(
        Path.cwd())[:str(Path.cwd()).rfind('/')]])
    assert res.exit_code == 0
    assert 'OK\n' == res.output


def test_post_1():
    res = cli_runner.invoke(POST, [f'{str(Path.cwd())}/client.py'])
    assert res.exit_code == 0
    assert 'Not required\n' == res.output


def test_post_2():
    res = cli_runner.invoke(
        POST, ['-p', '127.0.0.1:8001', f'{str(Path.cwd())}/client.py'])
    assert res.exit_code == 0
    assert 'Not required\n' == res.output


def test_delete_1():
    res = cli_runner.invoke(DELETE, ['client.py'])
    assert res.exit_code == 0
    assert 'OK\n' == res.output


def test_put_3():
    res = cli_runner.invoke(PUT, [f'{str(Path.cwd())}/client.py'])
    assert res.exit_code == 0
    assert 'OK\n' == res.output


def test_delete_2():
    res = cli_runner.invoke(DELETE, ['-p', '127.0.0.1:8001', 'client.py'])
    assert res.exit_code == 0
    assert 'OK\n' == res.output


def test_get_7():
    res = cli_runner.invoke(GET, [])
    assert res.exit_code == 0
    assert '[] OK\n' == res.output
