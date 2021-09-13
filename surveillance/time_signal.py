import time


class TimeSignal:
    def __init__(self) -> None:
        self._signals = []

    def notify(self):
        self._signals(time.time())

    def should_trigger(self):
        pass
    