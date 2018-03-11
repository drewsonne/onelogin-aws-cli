"""
Create a class to handle interrupts and runtime
"""
from threading import Event, Thread

from abc import ABCMeta, abstractmethod


class RuntimeThread(Thread, metaclass=ABCMeta):
    """
    Parent class to build a Thread with a runtime loop
    """

    def __init__(self, runtime_pause: int, name: str = None):
        super().__init__(name=name)
        self._period = runtime_pause

        self._running = False
        self._sleep = Event()

    def run(self):
        """
        Create a runtime for the foreground credentials renewal
        """
        self._running = True
        while self._running:
            self._sleep.wait(self._period)

            self.handle_run()

    @abstractmethod
    def handle_run(self):
        """
        Implement this method to contain the business logic to perform on each
            iteration of the runtime loop
        """
        pass

    def interrupt(self, signal_num: int, *args):
        """
        Received a shutdown signal.
        Could implement HUP to perform a SAML refresh or something though.
        :param signal_num:
        :param args:
        """

        self._sleep.set()

        print("Shutting down '{name}' process...".format(
            name=self.name
        ))

        self._running = False

        while self.is_alive():
            self._sleep.wait(1)

        print("Shutdown finished.")
