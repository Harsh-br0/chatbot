import os
from typing import Sequence

import dotenv

from .defaults import CONFIG_FILE


def ensure_envs(envs: Sequence[str]):
    if not dotenv.load_dotenv(CONFIG_FILE):
        raise RuntimeError("Failed to load the config file...")

    for env in envs:
        if os.getenv(env) is None:
            raise RuntimeError(f"env {env} not found...")


def chunk_iter(iterator, size=20):
    temp = []
    for item in iterator:
        temp.append(item)
        if len(temp) == size:
            yield temp
            temp.clear()
    if temp:
        yield temp
