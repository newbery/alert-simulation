import random
import string
import time

import numpy as np  # type: ignore
from scipy import stats  # type: ignore


def generate_message() -> str:
    """Return some random text up to 100 characters long"""
    length = random.randint(1, 100)
    return "".join(random.choices(string.ascii_letters, k=length))


def generate_phone_number() -> str:
    """Return a random phone number in the format XXX-XXX-XXXX"""
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 888)).zfill(3)
    last = str(random.randint(1, 9999)).zfill(4)
    return f"{first}-{second}-{last}"


def send_message(
    message: str,
    phone_number: str,
    failure_rate: float,
    delaydist: tuple[float, float, int],
) -> tuple[float, bool]:
    """Simulates sending an SMS message but doesn't actually do anything
    except sleep for some random time before returning the time and whether
    the send operation failed (also randomized).
    """
    start = time.perf_counter()
    random_sleep(*delaydist)
    failed = random.random() <= failure_rate
    delay = time.perf_counter() - start
    return delay, failed


def random_sleep(mean: float, stdev: float, seed: int) -> None:
    """Sleep for random amount of time, based on given mean & stdev.

    Since negative time doesn't make sense for this case, let's generate
    the delay from a truncated normal distribution which still gives us a
    well-behaved distribution around the desired mean.
    """
    lower_limit = -mean / stdev
    upper_limit = float("inf")
    truncnorm = stats.truncnorm(lower_limit, upper_limit, loc=mean, scale=stdev)
    np.random.seed(seed)
    time.sleep(truncnorm.rvs())
