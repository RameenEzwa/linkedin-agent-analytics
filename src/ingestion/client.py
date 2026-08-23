import time
from typing import Any

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


class LinkedInAPIError(Exception):
    """Raised when the LinkedIn API request fails."""


class LinkedInClient:
    def __init__(self, base_url: str, token: str = ""):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        if token:
            self.session.headers.update(
                {"Authorization": f"Bearer {token}"}
            )

    @retry(
        retry=retry_if_exception_type(
            (requests.RequestException, LinkedInAPIError)
        ),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = self.session.get(
            url,
            params=params,
            timeout=30,
        )

        # Rate limit
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")

            if retry_after:
                try:
                    time.sleep(float(retry_after))
                except ValueError:
                    time.sleep(2)
            else:
                time.sleep(2)

            raise LinkedInAPIError("LinkedIn API rate limit reached.")

        # Retry temporary server errors
        if response.status_code >= 500:
            raise LinkedInAPIError(
                f"LinkedIn API server error: {response.status_code}"
            )

        # Other errors
        if not response.ok:
            raise LinkedInAPIError(
                f"LinkedIn API request failed: {response.status_code}"
            )

        return response.json()