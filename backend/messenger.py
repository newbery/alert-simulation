import random
import string
import time

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
    delaydist: tuple[float, float],
) -> tuple[float, bool]:
    """Simulates sending an SMS message but doesn't actually do anything
    but sleep for some random time before returning the time and whether
    the send operation failed (also simulated).
    """
    start = time.perf_counter()
    random_sleep(*delaydist)
    failed = random.random() <= failure_rate
    delay = time.perf_counter() - start
    return delay, failed


def random_sleep(mean: float, stdev: float) -> None:
    """Sleep for random amount of time, based on given mean & stdev.

    Since negative time doesn't make sense for this case, let's generate
    the delay from a truncated normal distribution which still gives us a
    well-behaved distribution around the desired mean.

    TODO: The trunc_norm distribution should maybe be cached somewhere.
    Re-initializing it for each call to this function seems wasteful.
    """
    lower_limit = -mean / stdev
    upper_limit = float("inf")
    trunc_norm = stats.truncnorm(lower_limit, upper_limit, loc=mean, scale=stdev)
    time.sleep(trunc_norm.rvs())
