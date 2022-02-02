if __name__ == "__main__":
    from telegram.ext import CommandHandler, Updater, ConversationHandler, MessageHandler, Filters

    from app.config import TELEGRAM_TOKEN
    from app import handlers, constants

    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("help", handlers.start))
    dispatcher.add_handler(CommandHandler("start", handlers.start))
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("cache", handlers.cache_entrypoint),
                CommandHandler("filter", handlers.filter_entrypoint),
            ],
            states={
                constants.ACTION_CACHE_STICKERS: [MessageHandler(Filters.sticker, handlers.cache_stickers)],
                constants.ACTION_FILTER_STICKERS: [MessageHandler(Filters.sticker, handlers.filter_stickers)],
            },
            fallbacks=[CommandHandler("finish", handlers.finish)],
        )
    )
    dispatcher.add_error_handler(handlers.error)

    updater.start_polling()
    updater.idle()
