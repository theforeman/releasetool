import functools
import os
import shutil
import tempfile
import pytest
import releasetool


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fixtures',
)

TESTREPO_DIR = os.path.join(FIXTURE_DIR, 'testrepo')
MOCKBIN_DIR = os.path.join(FIXTURE_DIR, 'mockbin')
MOCK_SOURCES_DIR = os.path.join(FIXTURE_DIR, 'mock_sources')

DEFAULT_ARGS = []
if os.environ.get('TRAVIS', None):
    DEFAULT_ARGS.extend(['-e', 'ansible_remote_tmp=/tmp/ansible-remote'])


def obal_cli_test(func=None):
    if func is None:
        return functools.partial(obal_cli_test)

    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        __tracebackhide__ = True
        tempdir = tempfile.mkdtemp()
        repodir = os.path.join(tempdir, 'repo')
        shutil.copytree(TESTREPO_DIR, repodir)

        oldcwd = os.getcwd()
        oldpath = os.environ['PATH']
        os.chdir(repodir)
        os.environ['PATH'] = "{}:{}".format(MOCKBIN_DIR, oldpath)
        os.environ['MOCKBIN_LOG'] = os.path.join(tempdir, 'mockbin.log')

        func(*args, **kwargs)

        os.chdir(oldcwd)
        os.environ['PATH'] = oldpath
        os.environ.pop('MOCKBIN_LOG')

        shutil.rmtree(tempdir, ignore_errors=True)

    return func_wrapper


def run_obal(args, exitcode):
    with pytest.raises(SystemExit) as excinfo:
        releasetool.main(args + DEFAULT_ARGS)
    assert excinfo.value.code == exitcode


def assert_obal_success(args):
    run_obal(args, 0)


def assert_obal_failure(args):
    run_obal(args, 2)


def assert_mockbin_log(content):
    __tracebackhide__ = True
    expected_log = "\n".join(content)
    expected_log = expected_log.replace('{pwd}', os.getcwd())
    with open(os.environ['MOCKBIN_LOG']) as mockbinlog:
        log = mockbinlog.read().strip()
        assert log == expected_log


@obal_cli_test()
def test_obal_noargs():
    assert_obal_failure([])
