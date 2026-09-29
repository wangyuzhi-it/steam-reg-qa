"""LLM 客户端:DeepSeek(默认)/ OpenAI 兼容协议。"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

import requests

log = logging.getLogger(__name__)

PROVIDERS = {
    "deepseek": {
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
        "env_key": "DEEPSEEK_API_KEY",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
        "env_key": "OPENAI_API_KEY",
    },
}


class LLMError(RuntimeError):
    pass


class LLMClient:
    def __init__(self, provider: str = "deepseek", api_key: str | None = None,
                 timeout: int = 60, max_retries: int = 2):
        if provider not in PROVIDERS:
            raise ValueError(f"unknown provider: {provider}")
        cfg = PROVIDERS[provider]
        self.provider = provider
        self.model = cfg["model"]
        self.base_url = cfg["base_url"].rstrip("/")
        self.api_key = api_key or os.getenv(cfg["env_key"], "")
        self.timeout = timeout
        self.max_retries = max_retries

    @property
    def ready(self) -> bool:
        return bool(self.api_key)

    def chat_json(self, messages: list[dict], temperature: float = 0.3) -> dict[str, Any]:
        """调 chat completions,要求模型返回 JSON,并解析为 dict。"""
        if not self.ready:
            raise LLMError(f"{self.provider} api key missing, set the env var")

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        last_err: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
                if resp.status_code >= 500:
                    raise LLMError(f"upstream {resp.status_code}: {resp.text[:200]}")
                resp.raise_for_status()
                break
            except (requests.RequestException, LLMError) as e:
                last_err = e
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
                else:
                    raise LLMError(f"request failed after {self.max_retries + 1} tries: {e}") from e

        data = resp.json()
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise LLMError(f"bad response shape: {data}") from e

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            log.warning("model returned non-json: %s", content[:300])
            raise LLMError(f"model returned non-json: {e}") from e