from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from threading import RLock
from typing import Any


class EventBus:
    """Bus de eventos simple para comunicar ventanas dentro del mismo proceso."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[[dict[str, Any]], None]]] = defaultdict(list)
        self._lock = RLock()

    def subscribe(self, event_name: str, callback: Callable[[dict[str, Any]], None]) -> None:
        with self._lock:
            if callback not in self._listeners[event_name]:
                self._listeners[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable[[dict[str, Any]], None]) -> None:
        with self._lock:
            callbacks = self._listeners.get(event_name)
            if not callbacks:
                return
            if callback in callbacks:
                callbacks.remove(callback)
            if not callbacks:
                self._listeners.pop(event_name, None)

    def emit(self, event_name: str, payload: dict[str, Any] | None = None) -> None:
        with self._lock:
            callbacks = list(self._listeners.get(event_name, ()))

        evento = payload or {}
        for callback in callbacks:
            try:
                callback(evento)
            except Exception as e:
                import logging
                logging.error(f"Error in EventBus callback for event '{event_name}': {e}", exc_info=True)
                continue


event_bus = EventBus()