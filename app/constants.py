HELP_TEXT = (
    "I can find duplicates in sticker sets\n\n"
    "Use /cache to cache stickers from sticker set\n"
    "Use /filter to filter stickers from sticker set\n"
    "Use /finish to finish a cache / filter session"
)
END_SESSION_TEXT = (
    "Session was finished.\n\n"
    "Use /cache to cache stickers from sticker set\n"
    "Use /filter to filter stickers from sticker set"
)
CACHE_ACTION_HELP_TEXT = (
    "Send me a sticker from any sticker set and I'll cache the whole sticker set\n\n"
    "To finish the session type /finish"
)
FILTER_ACTION_HELP_TEXT = (
    "Send me a sticker from any sticker set and I'll filter given sticker set\n"
    "and send to you new filtered sticker set.\n\n"
    "To finish the session type /finish"
)

STICKER_SET_CACHING_SUCCESS_TEXT = "Stickers from {sticker_set_name} are cached!"
STICKER_SET_FILTERING_SUCCESS_TEXT = (
    "Stickers from {old_sticker_set_name} are filtered!\n\nTotal removed stickers: {total_removed_stickers}"
)

TASK_STARTED_TEXT = "Got it! Working... I will send you a message when I finish."
TASK_FAILED_ERROR_TEXT = "Sorry, I still working with given sticker set.\n\nI will send you a message when I finish"

INFO_FILENAME = "info"

STICKER_SET_NEW_NAME_TPL = "{sticker_set_old_name}_{rand_int}_by_{telegram_bot_name}"

ACTION_CACHE_STICKERS = 0
ACTION_FILTER_STICKERS = 1
