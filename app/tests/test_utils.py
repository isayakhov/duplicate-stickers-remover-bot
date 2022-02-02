import os
from unittest import mock

from app import config, constants, utils


def test_save_sticker_set_info_file(stickers_path, sticker_set_info):
    sticker_info = sticker_set_info.stickers_info[0]
    file_content = [
        f"{sticker_set_info.user_id}\n",
        f"{sticker_set_info.name}\n",
        f"{sticker_set_info.title}\n",
        f"{sticker_info.filename},{sticker_info.emoji},{sticker_info.filehash}\n",
    ]
    with mock.patch("builtins.open", mock.mock_open()) as mocked_file:
        utils.save_sticker_set_info_file(stickers_path=stickers_path, sticker_set_info=sticker_set_info)

    mocked_file.assert_called_with(os.path.join(stickers_path, constants.INFO_FILENAME), "w+", encoding="utf-8")
    mocked_file().truncate.assert_called_once_with(0)
    mocked_file().writelines.assert_called_once_with(file_content)


def test_get_sticker_set_info_by_path(mocker, stickers_path, sticker_set_info):
    mocker.patch("os.path.exists", return_value=True)

    sticker_info = sticker_set_info.stickers_info[0]
    file_content = (
        f"{sticker_set_info.user_id}\n"
        f"{sticker_set_info.name}\n"
        f"{sticker_set_info.title}\n"
        f"{sticker_info.filename},{sticker_info.emoji},{sticker_info.filehash}\n"
    )
    with mock.patch("builtins.open", mock.mock_open(read_data=file_content)) as mocked_file:
        actual_sticker_set_info = utils.get_sticker_set_info_by_path(stickers_path=stickers_path)

    mocked_file.assert_called_once_with(os.path.join(stickers_path, constants.INFO_FILENAME), "r", encoding="utf-8")
    assert actual_sticker_set_info == sticker_set_info


def test_copy_stickers(faker, mocker, tg_sticker_set):
    mocker.patch("app.utils.shutil.rmtree")
    mocker.patch("app.utils.os.makedirs")
    mocked_image = mocker.patch("app.utils.Image")
    mocked_imagehash = mocker.patch("app.utils.imagehash.average_hash")
    mocked_save_sticker_set_info = mocker.patch("app.utils.save_sticker_set_info_file")

    user_id = faker.pyint()

    expected_stickers_path = os.path.join(config.STICKERS_ROOT_DIRECTORY, str(user_id), tg_sticker_set.name)

    actual_stickers_path = utils.copy_stickers(user_id, tg_sticker_set)

    mocked_image.open.assert_called_once()
    mocked_imagehash.assert_called_once()
    mocked_save_sticker_set_info.assert_called_once()
    assert actual_stickers_path == expected_stickers_path


def test_remove_duplicate_stickers(faker, mocker):
    mocker.patch("app.utils.os.walk", return_value=[(faker.pystr(), "", "")])
    mocked_os_remove = mocker.patch("app.utils.os.remove")
    mocked_save_sticker_set_info_file = mocker.patch("app.utils.save_sticker_set_info_file")

    user_id = faker.pyint()
    stickers_path = faker.pystr()
    filename = faker.pystr()
    sticker_set_info = utils.StickerSetInfo(
        user_id=user_id,
        name=faker.pystr(),
        title=faker.pystr(),
        stickers_info=[
            utils.StickerInfo(
                filename=filename,
                filepath=os.path.join(stickers_path, filename),
                filehash="ffff0100007fffff",
                emoji=faker.pystr(),
            )
        ],
    )

    mocker.patch("app.utils.get_sticker_set_info_by_path", return_value=sticker_set_info)

    removed_duplicates = utils.remove_duplicate_stickers(user_id=user_id, stickers_path=stickers_path)

    mocked_os_remove.assert_called_once()
    mocked_save_sticker_set_info_file.assert_called_once()
    assert removed_duplicates == 1


def test_create_sticker_set(mocker, faker, tg_bot, user_id, stickers_path, sticker_set_info):
    rand_int = faker.pyint()
    mocker.patch("app.utils.randint", return_value=rand_int)
    mocker.patch("builtins.open", mock.mock_open(read_data=faker.binary()))

    sticker_info = utils.StickerInfo(
        filename=faker.pystr(),
        filepath=os.path.join(faker.pystr(), faker.pystr()),
        filehash=faker.pystr(),
        emoji=faker.pystr(),
    )
    sticker_set_info.stickers_info = [sticker_info for _ in range(2)]
    expected_new_sticker_set_name = constants.STICKER_SET_NEW_NAME_TPL.format(
        sticker_set_old_name=sticker_set_info.name, rand_int=rand_int, telegram_bot_name=config.TELEGRAM_BOT_NAME
    )

    mocker.patch("app.utils.get_sticker_set_info_by_path", return_value=sticker_set_info)

    actual_new_sticker_set_name = utils.create_sticker_set(bot=tg_bot, user_id=user_id, stickers_path=stickers_path)

    tg_bot.create_new_sticker_set.assert_called_once()
    tg_bot.add_sticker_to_set.assert_called_once()
    assert actual_new_sticker_set_name == expected_new_sticker_set_name
