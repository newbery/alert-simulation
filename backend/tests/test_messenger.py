import time
import pytest

from backend import messenger


def test_generate_message():
    """The 'generate_message' func should return random text"""
    messages = [messenger.generate_message() for _ in range(100)]

    assert len(messages) == len(set(messages))
    assert all(isinstance(m, str) for m in messages)


def test_generate_phone_number():
    """The 'generate_phone_number' func should return a random phone number"""
    numbers = [messenger.generate_phone_number() for _ in range(100)]

    assert len(numbers) == len(set(numbers))
    assert all(isinstance(m, str) for m in numbers)


def test_send_message(mocker, freezer):
    """The 'send_message' func should pretend to send a message, taking
    some random time to do so and randomly failing. The random sleep
    is tested elsewhere so we'll mock that behavior here.
    """

    def mock_sleep(seconds):
        return lambda x, y, z: freezer.tick(seconds)

    mocker.patch.object(messenger, "random_sleep", mock_sleep(123))
    delaydist = (0, 0, 0)

    # success case
    delay, failed = messenger.send_message("text", "1-111-1111", 0.0, delaydist)
    assert delay == 123
    assert failed is False

    # failure case
    delay, failed = messenger.send_message("text", "1-111-1111", 1.0, delaydist)
    assert delay == 123
    assert failed is True


@pytest.mark.freeze_time(auto_tick_seconds=200)
def test_random_sleep(mocker):
    """The 'random_sleep' func should sleep for some random time.
    Random is hard to test so we'll control the clock with freezegun.
    We also mock 'stats.truncnorm' since it slows down this test.

    TODO: Cache the truncnorm distribution somewhere so it doesn't add
    a skew to the sleep time in production.
    """
    # The value returned by truncnorm.rvs() is ignored because of freezegun
    stats = mocker.patch.object(messenger, "stats")
    stats.truncnorm.return_value = mocker.Mock(**{"rvs.return_value": 0})

    start = time.perf_counter()
    messenger.random_sleep(11, 1, 1)
    end = time.perf_counter()

    # We've checked the time three times above so the clock has advanced
    # three times, or just once between start and end.
    assert end - start == 200
