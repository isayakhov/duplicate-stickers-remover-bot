#!/usr/bin/env sh

case "$1" in
    "help")
        echo "DuplicateStickersRemoverBot"
        echo "Please use of next parameters to start: "
        echo "  > bot: Run bot"
        ;;
    "bot")
        echo "Running bot ..."
        python -m app.main
        ;;
    "")
        echo "No run parameter passed please use one of: [bot, help]"
        exit 1
        ;;
    *)
        echo "Unknown command '$1'. please use one of: [bot, help]"
        exit 1
        ;;
esac
