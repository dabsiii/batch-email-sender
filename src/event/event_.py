from src.event.event import Event


class Event_(Event):
    def __init__(self):
        self._functions = []

    def subscribe(self, function) -> None:
        self._functions.append(function)

    def publish(self, data) -> None:
        [function(data) for function in self._functions]
