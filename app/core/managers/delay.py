import random
import time


def delay(min_seconds: float= 1.0, max_seconds: float = 2.0):
    time.sleep(random.uniform(min_seconds, max_seconds))
