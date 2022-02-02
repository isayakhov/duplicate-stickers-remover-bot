import logging

from telegram import Bot

from . import constants, utils

logger = logging.getLogger(__name__)


def cache_stickers(bot: Bot, user_id: int, chat_id: int, sticker_set_name: str) -> None:
    logger.info("Trying to get sticker set %s data", sticker_set_name)
    sticker_set = bot.get_sticker_set(sticker_set_name)

    logger.info("Trying to cache stickers from sticker set: %s", sticker_set_name)
    utils.copy_stickers(user_id, sticker_set)

    bot.get_chat(chat_id).send_message(
        constants.STICKER_SET_CACHING_SUCCESS_TEXT.format(sticker_set_name=sticker_set_name)
    )

    logger.info("Finished copy stickers from sticker set: %s", sticker_set_name)


def filter_stickers(bot: Bot, user_id: int, chat_id: int, sticker_set_name: str) -> None:
    logger.info("Trying to get sticker set %s data", sticker_set_name)
    sticker_set = bot.get_sticker_set(sticker_set_name)

    logger.info("Trying to save stickers from sticker set: %s", sticker_set_name)
    stickers_path = utils.copy_stickers(user_id, sticker_set)

    logger.info("Trying to remove duplicates from sticker set: %s", sticker_set_name)
    total_removed_stickers = utils.remove_duplicate_stickers(user_id, stickers_path)

    bot.get_chat(chat_id).send_message(
        constants.STICKER_SET_FILTERING_SUCCESS_TEXT.format(
            old_sticker_set_name=sticker_set_name, total_removed_stickers=total_removed_stickers
        )
    )

    if total_removed_stickers > 0:
        logger.info("Trying to create filtered sticker set: %s", sticker_set_name)
        new_sticker_set_name = utils.create_sticker_set(bot, user_id, stickers_path)

        logger.info("Trying to get created sticker set %s and send sticker to user", new_sticker_set_name)
        new_sticker_set = bot.get_sticker_set(new_sticker_set_name)
        bot.get_chat(chat_id).send_sticker(new_sticker_set.stickers[-1])
