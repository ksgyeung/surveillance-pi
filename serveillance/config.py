from dataclasses import dataclass
import json
from os import path

@dataclass
class DCConfig:
    identifier: str
    cameraIndex: int
    register_host: str
    fps: int
    cwidth: int
    cheight: int

    smbhost: str
    username: str
    password: str
    twilio_sid: str
    twilio_token: str
    sms_destination: str
    sms_from: str
    terminator: str

def load_config():
    filepath = path.join(path.dirname(__file__), 'config.json')

    file = open(filepath)
    data = json.load(file)
    file.close()

    return DCConfig(
        identifier=data['identifier'],
        cameraIndex=data['cameraIndex'],
        register_host=data['register_host'],
        fps=data['fps'],
        cwidth=data['cwidth'],
        cheight=data['cheight'],

        smbhost=data['smbhost'],
        username=data['username'],
        password=data['password'],
        twilio_sid=data['twilio_sid'],
        twilio_token=data['twilio_token'],
        sms_destination=data['sms_destination'],
        sms_from=data['sms_from'],
        terminator=data['terminator']
    )