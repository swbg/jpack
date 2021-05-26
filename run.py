import os
import sys
import subprocess
import configparser

from pathlib import Path
from typing import Dict, Optional


def load_config(path: Path) -> Dict:
    config = {}
    with open(path, 'r') as f:
        for line in f.readlines():
            if line.strip():
                kv = line.split('=')
                if len(kv) != 2:
                    continue
                config[kv[0].strip()] = kv[1].strip()
    return config


def create_env(path: Path) -> Path:
    if not path.exists():
        subprocess.check_call([sys.executable, '-m', 'venv', path])
    return path / 'bin' / 'python'


def install_packages(executable: Path, requirements: Path) -> None:
    subprocess.check_call([executable, '-m', 'pip', 'install', '-r', requirements])


def run_setup(executable: Path, setup_path: Path) -> None:
    cwd = os.getcwd()
    os.chdir(setup_path.parent.absolute())
    setup_file = setup_path.name
    subprocess.check_call([executable, setup_file, 'develop'])
    os.chdir(cwd)


def run() -> None:
    data_path = Path(__file__).parent.absolute() / 'data'
    config = configparser.ConfigParser()
    config.read(data_path / 'config.txt')
    config = config['default']

    executable = create_env(data_path / 'env')
    install_packages(executable, data_path / 'requirements.txt')
    if config['setup_path']:
        run_setup(executable, Path(config['setup_path']))
    subprocess.check_call([executable, data_path / 'start_server.py'])


if __name__ == '__main__':
    run()
