from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from app.core.exceptions import AIServiceError
import logging

logger = logging.getLogger(__name__)


# Retry decorator for AI API calls
# Retries up to 3 times with exponential backoff
ai_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(AIServiceError),
    before_sleep=lambda retry_state: logger.warning(
        f"AI API call failed, retrying... (attempt {retry_state.attempt_number}/3)"
    )
)
