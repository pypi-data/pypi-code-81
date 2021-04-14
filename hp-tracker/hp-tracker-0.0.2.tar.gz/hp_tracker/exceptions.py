class TrackingNetworkError(Exception):
    """Exception raised for errors with network connection or target server."""

    def __init__(self):
        self.message = f"Network error"
        super().__init__(self.message)


class TrackingStatusError(Exception):
    """Exception raised for errors with tracking number.

    Attributes:
        track_no -- tracking number
    """

    def __init__(self, track_no):
        self.message = f"Tracking status unavailable for tracking number: {track_no}"
        super().__init__(self.message)
