from dataclasses import dataclass

@dataclass
class DCConfig:
    cameraIndex: int
    smbhost: str
    username: str
    password: str
    terminator: str

