from dataclasses import dataclass

from .frame import Frame

@dataclass
class _Node:
    id: int
    value: any
    previousNode: any
    nextNode: any

class FrameQueue:
    def __init__(self, max_capacity = 300) -> None:
        #buffer 10 secs
        #self._queue = np.empty(18000, dtype='object')
        self._id = 1
        self._start = None
        self._end = None
        self._length = 0
        self._max_capacity = max_capacity
        self._current = None

    
    def push(self, frame: Frame):
        if self._length >= self._max_capacity:
            self.pop()
        self._push(frame)


    def _push(self, frame: Frame):
        node = _Node(
            id=self._id,
            value=frame,
            previousNode=None,
            nextNode=None
        )

        if self._length == 0:
            self._start = node
            self._end = node
        else:
            node.previousNode = self._end
            self._end.nextNode = node
            self._end = node

        self._length +=  1
        self._id += 1

    def pop(self):
        if self._length == 0:
            raise IndexError('length = 0')

        ret = self._start
        self._start = ret.nextNode
        if self._start is None:
            self._end = None
        else:
            self._start.previousNode = None
            ret.nextNode = None

        self._length -= 1

        return ret.value, ret.id

    def __len__(self):
        return self._length

    def __getitem__(self, index) -> Frame:
        if index >= self._length:
            raise IndexError()

        node = self._start
        for _ in range(0, index):
            node = node.nextNode
        
        return node.value, node.id

    def __iter__(self):
        self._current = self._start
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        ret1, ret2 = self._current.value, self._current.id
        self._current = self._current.nextNode
        return ret1, ret2

    def _show(self):
        node = self._start
        while node is not None:
            print('[{} <- {} -> {}]'.format(
                node.previousNode.id if node.previousNode is not None else 'X',
                node.id,
                node.nextNode.id if node.nextNode is not None else 'X',
            ))
            node = node.nextNode
