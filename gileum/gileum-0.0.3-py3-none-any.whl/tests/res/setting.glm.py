import time

from gileum.test import MockGileum


setting = MockGileum(
    test_name="unittest@gileum",
    developer_name="jjj999",
    current_time=time.time(),
    glm_name="main",
)
