import time


class TimedCache:
    def __init__(self, seconds):
        self.seconds = seconds
        self.entries = {}

    def get(self, key):
        expires_at, value = self.entries.get(key, (0, None))
        if time.time() < expires_at:
            return value
        return None

    def set(self, key, value):
        self.entries[key] = (time.time() + self.seconds, value)
