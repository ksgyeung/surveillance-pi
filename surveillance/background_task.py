from threading import Thread, Condition

STATE_DEAD = -1
STATE_IDLE = 0
STATE_RUNNING = 1
STATE_RESULT_AVAILABLE = 2

class BackgroundTask:
    def __init__(self) -> None:
        self._state = STATE_IDLE
        self._func = None
        self._params = None
        self._result = None
        
        self._looping = True
        self._cv = Condition()
        self._thread = Thread(target=self._loop)
        self._thread.isDaemon = True
        self._thread.start()
        pass

    def state(self):
        return self._state

    def submit_task(self, function, *params):
        if self._state != STATE_IDLE:
            raise('state is not STATE_IDLE')

        self._state = STATE_RUNNING
        self._func = function
        self._params = params
        with self._cv:
            self._cv.notify()
        pass

    def result(self):
        return self._result

    def clear_result(self):
        self._result = None
        self._state = STATE_IDLE

    def _loop(self):
        while self._looping:
            with self._cv:
                self._cv.wait()
            if self._func is not None and self._result is None:
                try:
                    self._result = self._func(*self._params)
                    self._func = None
                    self._params = None
                    self._state = STATE_RESULT_AVAILABLE
                except Exception as e:
                    self._func = None
                    self._params = None
                    self._result = None
                    self._state = STATE_IDLE
                    print(e)

    def shutdown(self):
        self._looping = False
        self._func = None
        self._params = None
        self._result = None
        self._state = STATE_DEAD
        
        with self._cv:
            self._cv.notify()
        self._thread.join()
