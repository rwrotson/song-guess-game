import threading


def get_singleton_instance[T](cls: type[T]) -> T:
    if not hasattr(cls, "_instance"):
        with threading.Lock():
            if not hasattr(cls, "_instance"):
                cls._instance = cls()
    return cls._instance
