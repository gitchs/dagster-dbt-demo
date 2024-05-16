#!/usr/bin/env python3
import os
from pathlib import Path
from subprocess import Popen


DBT_TARGET_ROOT = Path('/workspace').joinpath('warehouse', 'target').absolute()

_DEFAULT_PATH = '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'


def check_rc(code: int):
    def wrapper0(method):
        def wrapper1(*args, **kwargs):
            rc = method(*args, **kwargs)
            if rc != code:
                raise RuntimeError('invalid return code: %d', rc)
        return wrapper1
    return wrapper0


@check_rc(0)
def init_project() -> int:
    child = Popen([
        '/usr/local/bin/poetry',
        'install',
    ])
    return child.wait()


@check_rc(0)
def init_sshd_authorized() -> int:
    ssh_root = Path.home().joinpath('.ssh')
    if not ssh_root.exists():
        ssh_root.mkdir(parents=True)
    ssh_authorized_file = ssh_root.joinpath('authorized_keys')
    ssh_public_key = os.getenv('SSH_PUBLIC_KEY')
    if ssh_public_key:
        with open(ssh_authorized_file, 'a', encoding='utf8') as output:
            output.write(f'# auto import ssh key\n{ssh_public_key}\n')
        os.chmod(ssh_authorized_file, 0o600)
    return 0


def start_sshd() -> Popen:
    runtime_dir = Path('/run/sshd')
    if not runtime_dir.exists():
        runtime_dir.mkdir(parents=True)
    child = Popen([
        '/usr/sbin/sshd',
        '-D',
        '-p', '22',
    ])
    return child


def start_dagster() -> Popen:
    env = {
        'DAGSTER_HOME': os.getenv('DAGSTER_HOME') or '/workspace/',
        'PATH': os.getenv('PATH') or _DEFAULT_PATH,
    }
    child = Popen([
        '/usr/local/bin/poetry',
        'run',
        'dagster',
        'dev',
        '-m', 'dagsterproject',
        '-m', 'dagster_example',
        '-h', '0.0.0.0'
    ], env=env, cwd=os.getcwd())
    return child


def start_dbt_docs_server() -> Popen:
    child = Popen([
        'python3',
        '-m', 'http.server'
    ], cwd=str(DBT_TARGET_ROOT))
    return child

def main():
    init_project()
    init_sshd_authorized()

    children = [
        start_sshd(),
        start_dagster(),
        start_dbt_docs_server(),
    ]
    for child in children:
        child.wait()


if __name__ == '__main__':
    main()
