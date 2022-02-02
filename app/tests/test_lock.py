from unittest import mock

from app import constants
from app.lock import lock


def test_run_in_thread_with_lock(faker, tg_bot, user_id, sticker_set_name):
    fake_func = mock.MagicMock()

    expected_response_text = constants.TASK_STARTED_TEXT.format(sticker_set_name=sticker_set_name)

    actual_response_text = lock.run_in_thread_with_lock(
        func=fake_func, bot=tg_bot, user_id=user_id, chat_id=faker.pyint(), sticker_set_name=sticker_set_name
    )

    fake_func.assert_called_once()
    assert actual_response_text == expected_response_text
