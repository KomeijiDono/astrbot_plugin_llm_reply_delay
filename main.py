import asyncio
import random
from typing import Any

from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.provider import LLMResponse
from astrbot.api.star import Context, Star, register


PLUGIN_NAME = "astrbot_plugin_llm_reply_delay"


def _as_non_negative_float(value: Any, default: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = default
    return max(number, 0.0)


@register(
    "llm_reply_delay",
    "KomeijiDono",
    "Delay LLM replies before sending them to the chat platform.",
    "1.0.0",
)
class LLMReplyDelayPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    def _config_get(
        self,
        group: str,
        key: str,
        default: Any,
        legacy_key: str | None = None,
    ) -> Any:
        group_config = self.config.get(group, {})
        if isinstance(group_config, dict) and key in group_config:
            return group_config.get(key, default)
        if legacy_key is not None and legacy_key in self.config:
            return self.config.get(legacy_key, default)
        return self.config.get(key, default)

    def _get_delay_seconds(self, text: str) -> float:
        mode = str(self._config_get("general", "delay_mode", "fixed") or "fixed").lower()

        if mode == "random":
            min_seconds = _as_non_negative_float(
                self._config_get(
                    "random_delay",
                    "min_seconds",
                    1.0,
                    "random_min_seconds",
                ),
                1.0,
            )
            max_seconds = _as_non_negative_float(
                self._config_get(
                    "random_delay",
                    "max_seconds",
                    5.0,
                    "random_max_seconds",
                ),
                5.0,
            )
            if min_seconds > max_seconds:
                min_seconds, max_seconds = max_seconds, min_seconds
            return random.uniform(min_seconds, max_seconds)

        if mode == "length":
            base_seconds = _as_non_negative_float(
                self._config_get(
                    "length_delay",
                    "base_seconds",
                    0.5,
                    "length_base_seconds",
                ),
                0.5,
            )
            per_char_seconds = _as_non_negative_float(
                self._config_get(
                    "length_delay",
                    "per_char_seconds",
                    0.03,
                    "length_per_char_seconds",
                ),
                0.03,
            )
            max_seconds = _as_non_negative_float(
                self._config_get(
                    "length_delay",
                    "max_seconds",
                    10.0,
                    "length_max_seconds",
                ),
                10.0,
            )
            return min(base_seconds + len(text) * per_char_seconds, max_seconds)

        return _as_non_negative_float(
            self._config_get("fixed_delay", "seconds", 2.0, "fixed_seconds"),
            2.0,
        )

    @filter.on_llm_response()
    async def on_llm_response(
        self,
        event: AstrMessageEvent,
        resp: LLMResponse,
    ) -> None:
        if not self._config_get("general", "enabled", True):
            return

        text = getattr(resp, "completion_text", "") or ""
        delay_seconds = self._get_delay_seconds(str(text))
        if delay_seconds <= 0:
            return

        logger.debug(
            f"[{PLUGIN_NAME}] delay LLM reply for {delay_seconds:.3f} seconds "
            f"before sending to {event.unified_msg_origin}"
        )
        await asyncio.sleep(delay_seconds)

    async def terminate(self) -> None:
        pass
