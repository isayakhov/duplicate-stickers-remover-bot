from unittest import mock

from telegram.ext import ConversationHandler

from app import constants, handlers
from app.lock import lock


def test_start_ok(tg_update, tg_context):
    handlers.start(tg_update, tg_context)

    tg_update.message.reply_text.assert_called_once_with(constants.HELP_TEXT)


def test_cache_stickers_ok(mocker, faker, tg_bot, tg_update, tg_context):
    expected_response = faker.pystr()

    mocker.patch.object(lock, "run_in_thread_with_lock", return_value=expected_response)
    mocker.patch("app.handlers.Bot", tg_bot)

    handlers.cache_stickers(tg_update, tg_context)

    tg_update.message.reply_text.assert_called_once_with(expected_response)


def test_filter_stickers_ok(mocker, faker, tg_bot, tg_update, tg_context):
    expected_response = faker.pystr()

    mocker.patch.object(lock, "run_in_thread_with_lock", return_value=expected_response)
    mocker.patch("app.handlers.Bot", tg_bot)

    handlers.filter_stickers(tg_update, tg_context)

    tg_update.message.reply_text.assert_called_once_with(expected_response)


def test_error_ok(mocker, tg_update, tg_context):
    logger_mock = mock.MagicMock(warning=mock.MagicMock())
    mocker.patch("app.handlers.logger", logger_mock)

    handlers.error(tg_update, tg_context)

    logger_mock.warning.assert_called_once()


def test_finish_ok(tg_update, tg_context):
    actual_response_value = handlers.finish(tg_update, tg_context)

    tg_update.message.reply_text.assert_called_once_with(constants.END_SESSION_TEXT)

    assert actual_response_value == ConversationHandler.END


def test_cache_entrypoint_ok(tg_update, tg_context):
    actual_response_value = handlers.cache_entrypoint(tg_update, tg_context)

    tg_update.message.reply_text.assert_called_once_with(constants.CACHE_ACTION_HELP_TEXT)

    assert actual_response_value == constants.ACTION_CACHE_STICKERS


def test_filter_entrypoint_ok(tg_update, tg_context):
    actual_response_value = handlers.filter_entrypoint(tg_update, tg_context)

    tg_update.message.reply_text.assert_called_once_with(constants.FILTER_ACTION_HELP_TEXT)

    assert actual_response_value == constants.ACTION_FILTER_STICKERS
