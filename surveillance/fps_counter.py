import time

class FpsCounter:
    def __init__(self) -> None:
        self._time = None
        self._count = 0
        self._history = []

    def tick(self, callback = None):
        now = int(time.time())
        if now != self._time:
            if callback is not None:
                callback(self._count)
            if self._count > 0:
                self._history.append(self._count)
            self._time = now
            self._count = 0
        self._count = self._count + 1

    def fps(self):
        return self._count


    def stat(self):
        return self._history