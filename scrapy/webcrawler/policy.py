from rotating_proxies.policy import BanDetectionPolicy
from twisted.internet.error import TimeoutError, TCPTimedOutError

class TimeoutBanPolicy(BanDetectionPolicy):
    """
    Custom ban policy that treats timeout exceptions as bans,
    preventing retries on the same proxy when timeouts occur.
    """
    def exception_is_ban(self, request, exception):
        # If it's a timeout, mark proxy as banned
        if isinstance(exception, (TimeoutError, TCPTimedOutError)):
            return True
        # Otherwise, defer to default logic
        return super().exception_is_ban(request, exception)

    def should_retry(self, request, exception=None, response=None):
        # Don’t retry timed-out requests with the same proxy
        if exception and isinstance(exception, (TimeoutError, TCPTimedOutError)):
            return False
        # Otherwise, use the default policy for retries
        return super().should_retry(request, exception=exception, response=response)
