import logging

from telegram import Bot, Update
from telegram.ext import CallbackContext, ConversationHandler

from . import config, constants, lock, services

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    assert context is not None
    assert update.message is not None

    logger.info("Trying to show help message")

    update.message.reply_text(constants.HELP_TEXT)

    logger.info("Finish start handler")


def cache_entrypoint(update: Update, context: CallbackContext) -> int:
    assert context is not None
    assert update.message is not None

    update.message.reply_text(constants.CACHE_ACTION_HELP_TEXT)

    return constants.ACTION_CACHE_STICKERS


def cache_stickers(update: Update, context: CallbackContext) -> None:
    assert context is not None
    assert update.message is not None
    assert update.message.from_user is not None
    assert update.message.sticker is not None
    assert update.message.sticker.set_name is not None

    logger.info("Start cache_stickers handler")

    update.message.reply_text(
        lock.lock.run_in_thread_with_lock(
            func=services.cache_stickers,
            bot=Bot(config.TELEGRAM_TOKEN),
            user_id=update.message.from_user.id,
            chat_id=update.message.chat_id,
            sticker_set_name=update.message.sticker.set_name,
        )
    )

    logger.info("Finish cache_stickers handler")


def filter_entrypoint(update: Update, context: CallbackContext) -> int:
    assert context is not None
    assert update.message is not None

    update.message.reply_text(constants.FILTER_ACTION_HELP_TEXT)

    return constants.ACTION_FILTER_STICKERS


def filter_stickers(update: Update, context: CallbackContext) -> None:
    assert context is not None
    assert update.message is not None
    assert update.message.from_user is not None
    assert update.message.sticker is not None
    assert update.message.sticker.set_name is not None

    logger.info("Start filter_stickers handler")

    update.message.reply_text(
        lock.lock.run_in_thread_with_lock(
            func=services.filter_stickers,
            bot=Bot(config.TELEGRAM_TOKEN),
            user_id=update.message.from_user.id,
            chat_id=update.message.chat_id,
            sticker_set_name=update.message.sticker.set_name,
        )
    )

    logger.info("Finish filter_stickers handler")


def error(update, context):
    logger.warning("Update '%s' caused error '%s'", update, context.error)


def finish(update: Update, context: CallbackContext) -> int:
    assert context is not None
    assert update.message is not None

    update.message.reply_text(constants.END_SESSION_TEXT)

    return ConversationHandler.END
