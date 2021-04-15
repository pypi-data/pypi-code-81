from dataclasses import dataclass


@dataclass(frozen=True)
class DockerImage:
    repository: str
    user: str
    name: str
    tag: str

    @property
    def image(self):
        return f"{self.repository}/{self.user}/{self.name}:{self.tag}"
