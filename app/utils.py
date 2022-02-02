import logging
import os
import shutil
from dataclasses import dataclass
from random import randint
from typing import List, Optional, Set

import imagehash
from PIL import Image
from telegram import Bot, StickerSet

from . import config, constants

logger = logging.getLogger(__name__)


@dataclass
class StickerInfo:
    filename: str
    filepath: str
    filehash: str
    emoji: Optional[str] = None
    removed: bool = False


@dataclass
class StickerSetInfo:
    user_id: int
    name: str
    title: str
    stickers_info: List[StickerInfo]


def save_sticker_set_info_file(stickers_path: str, sticker_set_info: StickerSetInfo) -> None:
    basic_info = [str(sticker_set_info.user_id) + "\n", sticker_set_info.name + "\n", sticker_set_info.title + "\n"]
    stickers_info = [
        f"{sticker_info.filename},{sticker_info.emoji},{sticker_info.filehash}\n"
        for sticker_info in sticker_set_info.stickers_info
        if not sticker_info.removed
    ]

    with open(os.path.join(stickers_path, constants.INFO_FILENAME), "w+", encoding="utf-8") as info_file:
        info_file.truncate(0)
        info_file.writelines(basic_info + stickers_info)


def get_sticker_set_info_by_path(stickers_path: str) -> Optional[StickerSetInfo]:
    filename = os.path.join(stickers_path, constants.INFO_FILENAME)

    if not os.path.exists(filename):
        return None

    with open(filename, "r", encoding="utf-8") as info_file:
        lines = info_file.readlines()

    sticker_set_info = StickerSetInfo(
        user_id=int(lines[0].strip()), name=lines[1].strip(), title=lines[2].strip(), stickers_info=[]
    )

    for sticker_info_line in lines[3:]:
        filename, emoji, filehash = sticker_info_line.strip().split(",")
        sticker_set_info.stickers_info.append(
            StickerInfo(
                filename=filename.strip(),
                filepath=os.path.join(stickers_path, filename.strip()),
                filehash=filehash.strip(),
                emoji=emoji.strip(),
            )
        )

    return sticker_set_info


def copy_stickers(user_id: int, sticker_set: StickerSet) -> str:
    stickers_path = os.path.join(config.STICKERS_ROOT_DIRECTORY, str(user_id), sticker_set.name)

    shutil.rmtree(stickers_path, ignore_errors=True)
    os.makedirs(stickers_path, exist_ok=True)

    sticker_set_info = StickerSetInfo(
        user_id=user_id, name=sticker_set.name, title=sticker_set.title, stickers_info=[]
    )

    for idx, sticker in enumerate(sticker_set.stickers):
        if sticker.is_animated:
            continue

        filename = f"{idx}.png"
        filepath = os.path.join(stickers_path, filename)

        sticker.get_file().download(filepath)
        filehash = imagehash.average_hash(Image.open(filepath))

        sticker_set_info.stickers_info.append(
            StickerInfo(filename=filename, filepath=filepath, filehash=str(filehash), emoji=sticker.emoji)
        )

    save_sticker_set_info_file(stickers_path, sticker_set_info)

    return stickers_path


def remove_duplicate_stickers(user_id: int, stickers_path: str) -> int:
    sticker_set_info = get_sticker_set_info_by_path(stickers_path)
    if not sticker_set_info:
        logger.warning("Can't find info file for given stickers path: %s", stickers_path)
        return 0

    existing_images_hashes: Set[imagehash.ImageHash] = set()
    for dirpath, _, _ in os.walk(os.path.join(config.STICKERS_ROOT_DIRECTORY, str(user_id))):
        current_sticker_set_info = get_sticker_set_info_by_path(dirpath)
        if dirpath == stickers_path or not current_sticker_set_info:
            continue

        existing_images_hashes.update(
            {imagehash.hex_to_hash(sticker_info.filehash) for sticker_info in current_sticker_set_info.stickers_info}
        )

    total_removed_stickers = 0
    for sticker_info in sticker_set_info.stickers_info:
        filehash = imagehash.hex_to_hash(sticker_info.filehash)
        for existing_image_hash in existing_images_hashes:
            if filehash - existing_image_hash < config.AVERAGE_HASH_THRESHOLD_VALUE:
                logger.info("Duplicated file %s was found and removed", sticker_info.filepath)
                sticker_info.removed = True
                os.remove(sticker_info.filepath)
                total_removed_stickers += 1
                break

    save_sticker_set_info_file(stickers_path, sticker_set_info)

    return total_removed_stickers


def create_sticker_set(bot: Bot, user_id: int, stickers_path: str) -> str:
    sticker_set_info = get_sticker_set_info_by_path(stickers_path)

    if not sticker_set_info or not sticker_set_info.stickers_info:
        raise ValueError(
            f"Can't find info file for given stickers path {stickers_path} or there are no stickers to create"
        )

    sticker_set_new_name = constants.STICKER_SET_NEW_NAME_TPL.format(
        sticker_set_old_name=sticker_set_info.name,
        rand_int=randint(0, 100),
        telegram_bot_name=config.TELEGRAM_BOT_NAME,
    )

    logger.info("Trying to create sticker set with name %s", sticker_set_new_name)

    with open(sticker_set_info.stickers_info[0].filepath, "rb") as image_file:
        image_bytes = image_file.read()

    bot.create_new_sticker_set(
        user_id=user_id,
        name=sticker_set_new_name,
        title=sticker_set_info.title,
        emojis="".join([sticker_info.emoji or "" for sticker_info in sticker_set_info.stickers_info]),
        png_sticker=image_bytes,
    )

    for sticker_info in sticker_set_info.stickers_info[1:]:
        logger.info("Trying to add image %s to sticker set", sticker_info.filepath)

        with open(sticker_info.filepath, "rb") as image_file:
            image_bytes = image_file.read()

        bot.add_sticker_to_set(
            user_id=user_id, name=sticker_set_new_name, emojis=sticker_info.emoji, png_sticker=image_bytes
        )

    return sticker_set_new_name
