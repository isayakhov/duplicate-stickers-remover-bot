from app import services


def test_cache_stickers(mocker, faker, tg_bot, user_id, chat_id, sticker_set_name):
    mocked_copy_stickers = mocker.patch("app.services.utils.copy_stickers", return_value=faker.pystr())

    services.cache_stickers(bot=tg_bot, user_id=user_id, chat_id=chat_id, sticker_set_name=sticker_set_name)

    mocked_copy_stickers.assert_called_once()
    tg_bot.get_sticker_set.assert_called_once()
    tg_bot.get_chat.assert_called_once()


def test_filter_stickers(mocker, faker, tg_bot, user_id, chat_id, sticker_set_name):
    mocked_copy_stickers = mocker.patch("app.services.utils.copy_stickers", return_value=faker.pystr())
    mocked_remove_duplicate_stickers = mocker.patch(
        "app.services.utils.remove_duplicate_stickers", return_value=faker.pyint()
    )
    mocked_create_sticker_set = mocker.patch("app.services.utils.create_sticker_set", return_value=faker.pyint())

    services.filter_stickers(bot=tg_bot, user_id=user_id, chat_id=chat_id, sticker_set_name=sticker_set_name)

    mocked_copy_stickers.assert_called_once()
    mocked_remove_duplicate_stickers.assert_called_once()
    mocked_create_sticker_set.assert_called_once()
    tg_bot.get_sticker_set.assert_called()
    tg_bot.get_chat.assert_called()
