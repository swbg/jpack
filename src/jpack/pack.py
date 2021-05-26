import sys
import shutil
import logging
import argparse

from pathlib import Path


INPUT_NOTEBOOK = Path('../../examples/basic.ipynb')
RUN_SCRIPT = Path('run.py')
REQUIREMENTS_FILE = Path('../../requirements.txt')
OUTPUT_FOLDER = Path('../../examples/basic')


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description='Pack a Jupyter notebook')
    parser.add_argument(
        '--name',
        type=str
    )
    parser.add_argument(
        '--backend',
        type=str,
        default='voila'
    )
    parser.add_argument(
        '--backend-args',
        type=str,
        default='--template = flex'
    )
    parser.add_argument(
        '--flex',
        dest='flex',
        action='store_true'
    )
    parser.add_argument(
        '--notebook-path',
        type=str
    )
    parser.add_argument(
        '--setup-path',
        type=str
    )
    parser.add_argument(
        '--add-path',
        type=str
    )

    parser.add_argument(
        '--requirements',
        type=str
    )
    parser.add_argument(
        '--output',
        type=str,
        default='.'
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)

    if not INPUT_NOTEBOOK.exists():
        raise FileNotFoundError('Input notebook not found')
    if OUTPUT_FOLDER.exists():
        # raise FileExistsError('Output folder already exists')
        # For debugging
        shutil.rmtree(OUTPUT_FOLDER)

    (OUTPUT_FOLDER / 'data').mkdir(parents=True)
    shutil.copy(INPUT_NOTEBOOK, OUTPUT_FOLDER / 'data')
    shutil.copy(REQUIREMENTS_FILE, OUTPUT_FOLDER / 'data')
    shutil.copy(RUN_SCRIPT, OUTPUT_FOLDER)
