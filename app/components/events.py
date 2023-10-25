from enum import Enum, auto
from typing import Callable, Any
from collections import defaultdict

Function = Callable[[Any], Any]


class EventType(Enum):
    DataPointsUpdated = auto()
    LabelsUpdated = auto()


subscribers: dict[EventType, list[Function]] = defaultdict(list)


def subscribe(event_type: EventType, fn: Function) -> None:
    subscribers[event_type].append(fn)


def post_event(event_type: EventType, data: Any) -> None:
    if not event_type in subscribers:
        return
    for fn in subscribers[event_type]:
        fn(data)
