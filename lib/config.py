import json
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class ConfigEntry:
    url: str
    token: str | None

class Config:
    _path: Path
    _entry: ConfigEntry
    
    def __init__(self, path: Path = Path('config.json')) -> None:
        self._path = path
        if not path.is_file():
            default_config = {
                "url": "http://127.0.0.1:9876",
                "token": None
            }
            with open(path, 'wt', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=4)
            self._entry = ConfigEntry(**default_config)
        else:
            with open(path, encoding='utf-8') as f:
                config = json.load(f)
            self._entry = ConfigEntry(**config)
            
    @property
    def url(self) -> str:
        return self._entry.url
    
    @property
    def token(self) -> str | None:
        return self._entry.token
