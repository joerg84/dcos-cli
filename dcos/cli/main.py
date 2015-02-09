"""
Usage:
    dcos <command> [<args>...]

Options:
    -h, --help           Show this screen
    --version            Show version

'dcos help --all' lists available subcommands. See 'dcos <command> --help' to
read about a specific subcommand.
"""


import os
import subprocess

import docopt
from dcos.api import constants, util


def main():
    if not _is_valid_configuration():
        return 1

    args = docopt.docopt(
        __doc__,
        version='dcos version {}'.format(constants.version),
        options_first=True)

    command = util.which(
        '{}{}'.format(constants.DCOS_COMMAND_PREFIX, args['<command>']))
    if command is not None:
        argv = [args['<command>']] + args['<args>']
        return subprocess.call([command] + argv)
    else:
        print(
            "{!r} is not a dcos command. See 'dcos --help'.".format(
                args['<command>']))
        return 1


def _is_valid_configuration():
    """Validates running environment

    :returns: True if the environment is configure correctly, False otherwise.
    :rtype: bool
    """

    dcos_path = os.environ.get(constants.DCOS_PATH_ENV)
    if dcos_path is None:
        msg = 'Environment variable {!r} not set to the DCOS CLI path.'
        print(msg.format(constants.DCOS_PATH_ENV))
        return False

    if not os.path.isdir(dcos_path):
        msg = ('Environment variable {!r} maps to {!r} which is not a '
               'directory.')
        print(msg.format(constants.DCOS_PATH_ENV, dcos_path))
        return False

    dcos_config = os.environ.get(constants.DCOS_CONFIG_ENV)
    if dcos_config is None:
        msg = 'Environment variable {!r} must be set to the DCOS config file.'
        print(msg.format(constants.DCOS_CONFIG_ENV))
        return False

    if not os.path.isfile(dcos_config):
        msg = 'Environment variable {!r} maps to {!r} and it is not a file.'
        print(msg.format(constants.DCOS_CONFIG_ENV, dcos_config))
        return False

    path = os.environ.get(constants.PATH_ENV)
    if path is None:
        msg = 'Environment variable {!r} not set.'
        print(msg.format(constants.PATH_ENV))
        return False

    return True
