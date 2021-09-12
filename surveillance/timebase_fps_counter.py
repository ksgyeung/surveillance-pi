import time


class TimeBaseFpsCounter:
    def __init__(self) -> None:
        self._time = None
        self._history = []

    def __enter__(self):
        self._time1 = time.time_ns()

    def __exit__(self, type, value, traceback):
        self._history.append(time.time_ns() - self._time1)

    def stat(self):
        ret = list(filter(lambda x: x > 0, self._history))
        return list(map(lambda x: 1 / (x / (10 ** 9)), ret))

