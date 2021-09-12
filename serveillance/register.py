import requests
from git import Repo
from os import path

from .config import load_config

def register():
    config = load_config()
    url = config.register_host + '/register'

    project_folder = path.basename(path.abspath(__file__))
    repo = Repo(path=project_folder)

    body = {
        'identifier': config.identifier,
        'commit': repo.head.object.hexsha,
    }

    requests.post(url, data=body)

def keep_alive():
    config = load_config()
    url = config.register_host + '/keepalive'
    
    body = {
        'identifier': config.identifier,
    }
    requests.post(url, data=body)

def unregister():
    config = load_config()
    url = config.register_host + '/unregister'
    
    body = {
        'identifier': config.identifier,
    }
    requests.post(url, data=body)
