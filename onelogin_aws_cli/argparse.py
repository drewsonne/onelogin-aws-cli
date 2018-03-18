"""
Argument Parser
"""

import argparse
import os

import pkg_resources


class OneLoginAWSArgumentParser(argparse.ArgumentParser):
    """Argument Parser separated into daemon and cli tool"""

    def __init__(self):
        super().__init__(description='Login to AWS with OneLogin')

        self.add_argument(
            '-C', '--config-name',
            action=EnvDefault, required=False,
            dest='config_name',
            help='Switch configuration name within config file'
        )

        self.add_argument(
            '--profile',
            action=EnvDefault, required=False,
            help='Specify profile name of credential',
        )

        self.add_argument(
            '-u', '--username',
            action=EnvDefault, required=False,
            help='Specify OneLogin username'
        )

        self.add_argument(
            '-d', '--duration-seconds', type=int, default=3600,
            dest='duration_seconds',
            action=EnvDefault, required=False,
            help='Specify duration seconds which depend on IAM role session '
                 'duration: https://aws.amazon.com/about-aws/whats-new/2018'
                 '/03/longer-role-sessions/'
        )

        version = pkg_resources.get_distribution(__package__).version
        self.add_argument(
            '-v', '--version', action='version',
            version="%(prog)s " + version
        )

        renew_seconds_group = self.add_mutually_exclusive_group()

        renew_seconds_group.add_argument(
            '-r', '--renew-seconds', type=int,
            action=EnvDefault, required=False,
            help='Auto-renew credentials after this many seconds'
        )

        renew_seconds_group.add_argument(
            # Help is suppressed as this is replaced by the POSIX friendlier
            # version above. This is here for legacy compliance and will
            # be deprecated.
            '--renewSeconds', type=int, help=argparse.SUPPRESS,
            action=EnvDefault, required=False,
            dest='renew_seconds_legacy'
        )

        self.add_argument(
            '-c', '--configure', dest='configure', action='store_true',
            help='Configure OneLogin and AWS settings'
        )


class EnvDefault(argparse.Action):
    """Allow argparse values to be pulled from environment variables"""

    def __init__(self, required=True, default=None, **kwargs):

        if 'dest' in kwargs:
            name = 'ONELOGIN_AWS_CLI_' + kwargs['dest'].upper()
            # Fall back to the explicit command line default.
            default = os.environ.get(name, default)
            if 'type' in kwargs and default is not None:
                default = kwargs['type'](default)

        super().__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)