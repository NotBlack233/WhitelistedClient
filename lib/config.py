import json
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class ConfigEntry:
    url: str
    token: str | None


def load_config(path: Path = Path('config.json')) -> ConfigEntry:
    if not path.is_file():
        default_config = ConfigEntry(
            url="http://127.0.0.1:9876",
            token=None
        )
        with open(path, 'wt', encoding='utf-8') as f:
            json.dump(default_config.__dict__, f, ensure_ascii=False, indent=4)
        return default_config
    else:
        with open(path, encoding='utf-8') as f:
            config = json.load(f)
        return ConfigEntry(**config)
