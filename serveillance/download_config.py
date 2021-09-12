from dataclasses import dataclass

@dataclass
class DownloadedConfig:
    smbhost: str
    username: str
    password: str
    twilio_sid: str
    twilio_token: str
    sms_destination: str
    sms_from: str
    terminator: str