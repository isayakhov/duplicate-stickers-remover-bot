# Duplicate Stickers Remover Telegram Bot

[![build](https://github.com/isayakhov/duplicate-stickers-remover-bot/workflows/Linters%20And%20Tests/badge.svg)](https://github.com/isayakhov/duplicate-stickers-remover-bot/blob/main/.github/workflows/lint-and-tests.yml)
[![codecov](https://codecov.io/gh/isayakhov/duplicate-stickers-remover-bot/branch/master/graph/badge.svg?token=I7OA0CI4TU)](https://codecov.io/gh/isayakhov/duplicate-stickers-remover-bot)
[![code_quality](https://api.codiga.io/project/30890/score/svg)](https://app.codiga.io/project/30890/dashboard)
[![code_score](https://api.codiga.io/project/30890/status/svg)](https://app.codiga.io/project/30890/dashboard)

## What is this?

Bot can cache your stickers and then find duplicates in different sticker sets. When duplicates found bot will create new sticker set without duplicates and sends it to you. You will be the owner of all created sticker sets. Bot uses [average hash algorithm](http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html) from this [library](https://github.com/JohannesBuchner/imagehash) to find duplicates.

## How to run it locally?

1. First you need to create your own bot in Telegram.
2. Next you need to pass to environment variables your bot's token into `TELEGRAM_TOKEN` variable and your bot's name into `TELEGRAM_BOT_NAME` variable as well.
3. Run: `python -m app.main`.
4. Or build docker image and run it.
5. That's all :)

## How to use it?

To start caching sesstion type `/cache` and then send stickers from your sticker sets. Bot will cache whole sticker set and send you a message when it finished.

To fihish caching session type `/finish`.

To start filtering sesstion type `/filter` and then send stickers from your sticker sets. Bot will find and remove duplicates by early cached stickers from other sticker sets and create new sticker set with filtered stickers with same name. You will be the owner of created sticker sets.

To fihish filtering session type `/finish`.

## How to contribute?

1. Type: `pip install pre-commit && pre-commit install`
2. Make and commit your changes
3. Push your changes
4. Open Pull request

## Environment variables

### Common

|Name     | Required | Default | Description|
|:--------|:-------- |:------- |:-----------|
| STICKERS_ROOT_DIRECTORY      | - | same as app dir | Cache root directory             |
| AVERAGE_HASH_THRESHOLD_VALUE |   | 8               | Threshold value for average hash |

### Telegram

|Name     | Required | Default | Description|
|:--------|:-------- |:------- |:-----------|
| TELEGRAM_TOKEN    | - | "FILL_ME" | Telegram bot token |
| TELEGRAM_BOT_NAME | - | "FILL_ME" | Telegram bot name  |
