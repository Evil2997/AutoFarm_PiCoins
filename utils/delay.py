import random
import time


def delay(min_seconds: float, max_seconds: float):
    time.sleep(random.uniform(min_seconds, max_seconds))
