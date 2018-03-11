"""
Provide the foreground Process as a Thread
"""

from onelogin_aws_cli import OneloginAWS
from onelogin_aws_cli.daemon.runtime import RuntimeThread


class ForegroundProcess(RuntimeThread):
    """
    Run the credentials renewal process in a process
    """

    def __init__(self, period: int, api: OneloginAWS):
        super().__init__(period, name="FederatedAuthProcess")
        self._api = api

    def handle_run(self):
        """
        Call save credentials during our runtime
        """

        # @TODO We should check if the credentials are going to expire
        # in the immediate future, rather than constantly hitting
        # the AWS API.
        self._api.save_credentials()
