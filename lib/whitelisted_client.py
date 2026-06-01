import requests
import json
from enum import IntEnum
from uuid import UUID
from typing import Optional
from dataclasses import dataclass

class ErrorCode(IntEnum):
    UNKNOWN = 0
    INVALID_TOKEN = 101
    INVALID_ARGUMENT = 102
    MOJANG_API_NOT_FOUND = 1001
    MOJANG_API_TOO_MANY_REQUESTS = 1002
    WHITELIST_DUPLICATE_ENTRY = 1003
    WHITELIST_NOT_FOUND = 1004

@dataclass(frozen=True, kw_only=True)
class ProfileEntry:
    uuid: UUID
    name: str
    timestamp: int

class WhitelistedClient:
    def __init__(self, url: str, token: Optional[str] = None) -> None:
        self.url = url.removesuffix('/')
        self.token = token
        
    def add(self, uuid: Optional[UUID] = None, name: Optional[str] = None) -> ProfileEntry:
        res = requests.get(f'{self.url}/add', {
            "token": self.token,
            "uuid": str(uuid),
            "name": name,
        })
        content = json.loads(res.content.decode())
        if res.status_code != 200:
            raise RuntimeError(f'add failed: got status code {res.status_code}, message: {content["errorMessage"]}')
        return ProfileEntry(**content['data'])
    
    def remove(self, uuid: Optional[UUID] = None, name: Optional[str] = None):
        res = requests.get(f'{self.url}/remove', {
            "token": self.token,
            "uuid": str(uuid),
            "name": name,
        })
        content = json.loads(res.content.decode())
        if res.status_code != 200:
            raise RuntimeError(f'remove failed: got status code {res.status_code}, message: {content["errorMessage"]}')
    
    def query(self, uuid: Optional[UUID] = None, name: Optional[str] = None, timestamp: Optional[int] = None) -> bool:
        res = requests.get(f'{self.url}/query', {
            "token": self.token,
            "uuid": str(uuid),
            "name": name,
            "timestamp": timestamp
        })
        content = json.loads(res.content.decode())
        if res.status_code != 200:
            raise RuntimeError(f'query failed: got status code {res.status_code}, message: {content["errorMessage"]}')
        return content['data']
        
    def listAll(self) -> list[ProfileEntry]:
        res = requests.get(f'{self.url}/list', {
            "token": self.token
        })
        content = json.loads(res.content.decode())
        if res.status_code != 200:
            raise RuntimeError(f'listAll failed: got status code {res.status_code}, message: {content["errorMessage"]}')
        data: list = content['data']
        
        return [ProfileEntry(uuid=i['uuid'], name=i['name'], timestamp=i['timestamp']) for i in data]
    