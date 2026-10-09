class Stack:
    """
    LIFO structure backed by a plain Python list.
    """
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def clear(self):
        self._items.clear()

    def to_list(self):
        return list(self._items)

class GuessHistory:
    """
    Ordered record backed by a plain Python list.
    """
    def __init__(self):
        self._history = []

    def add(self, entry):
        self._history.append(entry)

    def remove_last(self):
        if self.size() > 0:
            return self._history.pop()
        return None

    def get_all(self):
        return self._history

    def get_last(self):
        if self.size() > 0:
            return self._history[-1]
        return None

    def get_previous(self):
        if self.size() > 1:
            return self._history[-2]
        return None

    def size(self):
        return len(self._history)

    def clear(self):
        self._history.clear()
