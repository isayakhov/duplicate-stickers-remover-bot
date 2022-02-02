# pylint: disable=redefined-outer-name
import os
from collections import defaultdict
from unittest import mock

import pytest

from app.lock import lock
from app.utils import StickerInfo, StickerSetInfo


@pytest.fixture(autouse=True, scope="function")
def reset_lock():
    lock.locked_sticker_sets = defaultdict(set)


@pytest.fixture
def chat_id(faker):
    return faker.pyint()


@pytest.fixture
def user_id(faker):
    return faker.pyint()


@pytest.fixture
def sticker_set_name(faker):
    return faker.pystr()


@pytest.fixture
def stickers_path(faker):
    return faker.pystr()


@pytest.fixture
def filename(faker):
    return faker.file_name()


@pytest.fixture
def sticker_set_info(faker, stickers_path, filename):
    sticker_info = StickerInfo(
        filename=filename, filepath=os.path.join(stickers_path, filename), filehash=faker.pystr(), emoji=faker.pystr()
    )
    return StickerSetInfo(user_id=faker.pyint(), name=faker.pystr(), title=faker.pystr(), stickers_info=[sticker_info])


@pytest.fixture
def tg_update(chat_id):
    return mock.MagicMock(message=mock.MagicMock(chat_id=chat_id, reply_text=mock.MagicMock()))


@pytest.fixture
def tg_context(sticker_set_name):
    return mock.MagicMock(args=[sticker_set_name])


@pytest.fixture
def tg_bot(faker):
    # bot.get_chat(chat_id).send_message()
    # bot.get_chat(chat_id).send_sticker()
    # bot.create_new_sticker_set()
    # bot.add_sticker_to_set()
    # bot.get_sticker_set()
    return mock.MagicMock(
        get_chat=mock.MagicMock(
            return_value=mock.MagicMock(
                send_message=mock.MagicMock(return_value=None), send_sticker=mock.MagicMock(return_value=None)
            )
        ),
        create_new_sticker_set=mock.MagicMock(),
        add_sticker_to_set=mock.MagicMock(),
        get_sticker_set=mock.MagicMock(stickers=[faker.pystr()]),
    )


@pytest.fixture
def tg_sticker_set(faker):
    # sticker_set.name
    # sticker_set.title
    # sticker_set.stickers[0].get_file().download(filepath)
    # sticker_set.stickers[0].is_animated
    # sticker_set.stickers[0].emoji
    return mock.MagicMock(
        name=faker.pystr(),
        title=faker.pystr(),
        stickers=[
            mock.MagicMock(
                emoji=faker.pystr(),
                is_animated=False,
                get_file=mock.MagicMock(return_value=mock.MagicMock(download=mock.MagicMock(return_value=True))),
            )
        ],
    )
