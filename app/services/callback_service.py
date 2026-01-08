import logging
import httpx

from app.models.response import CallbackPayload
from app.core.exceptions import CallbackError

logger = logging.getLogger(__name__)


class CallbackService:
    """Sends analysis results back to Spring server"""

    def __init__(self):
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def send_result(self, callback_url: str, payload: CallbackPayload):
        """
        Send analysis result to Spring's PATCH endpoint

        Args:
            callback_url: Spring endpoint URL (e.g., http://spring-server/api/reports/100)
            payload: CallbackPayload containing status and result/error

        Raises:
            CallbackError: If callback request fails
        """
        try:
            logger.info(f"Sending callback to {callback_url}")
            logger.debug(f"Payload: {payload.model_dump()}")

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.patch(
                    callback_url,
                    json=payload.model_dump(),
                    headers={"Content-Type": "application/json"}
                )

                response.raise_for_status()

                logger.info(f"Callback successful: {response.status_code}")

        except httpx.HTTPStatusError as e:
            logger.error(f"Callback HTTP error: {e.response.status_code} - {e.response.text}")
            raise CallbackError(f"HTTP {e.response.status_code}: {e.response.text}")

        except httpx.RequestError as e:
            logger.error(f"Callback request error: {e}")
            raise CallbackError(f"Request failed: {e}")

        except Exception as e:
            logger.error(f"Unexpected callback error: {e}")
            raise CallbackError(f"Unexpected error: {e}")
