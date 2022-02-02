import logging
import threading
from collections import defaultdict
from typing import Callable, Dict, Set

from telegram import Bot

from . import constants

logger = logging.getLogger(__name__)


class Lock:
    def __init__(self) -> None:
        self.locked_sticker_sets: Dict[int, Set[str]] = defaultdict(set)

    def lock_sticker_set(self, user_id: int, sticker_set_name: str) -> None:
        self.locked_sticker_sets[user_id].add(sticker_set_name)

    def is_sticker_set_locked(self, user_id: int, sticker_set_name: str) -> bool:
        return sticker_set_name in self.locked_sticker_sets[user_id]

    def unlock_sticker_set(self, user_id: int, sticker_set_name: str) -> None:
        self.locked_sticker_sets[user_id].discard(sticker_set_name)

    def _run_with_lock(self, func: Callable, bot: Bot, user_id: int, chat_id: int, sticker_set_name: str):
        self.lock_sticker_set(user_id, sticker_set_name)
        try:
            func(bot=bot, user_id=user_id, chat_id=chat_id, sticker_set_name=sticker_set_name)
        except Exception as exc:
            logger.exception(exc)
            bot.get_chat(chat_id).send_message(
                constants.TASK_FAILED_ERROR_TEXT.format(sticker_set_name=sticker_set_name)
            )
        finally:
            self.unlock_sticker_set(user_id, sticker_set_name)

    def run_in_thread_with_lock(
        self, func: Callable, bot: Bot, user_id: int, chat_id: int, sticker_set_name: str
    ) -> str:
        if self.is_sticker_set_locked(user_id, sticker_set_name):
            return constants.TASK_FAILED_ERROR_TEXT

        threading.Thread(
            target=self._run_with_lock,
            kwargs=dict(func=func, bot=bot, user_id=user_id, chat_id=chat_id, sticker_set_name=sticker_set_name),
        ).start()

        return constants.TASK_STARTED_TEXT.format(sticker_set_name=sticker_set_name)


lock = Lock()
