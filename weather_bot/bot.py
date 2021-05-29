from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.parsemode import ParseMode
import hydra
from omegaconf import DictConfig
import logging
from weather_bot.weather import WeatherReciever


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет, кот! Мур-мяу)"
    )


weather_reciever = None  # TODO: remove from global memory
def weather(update, context):
    for weather_text in weather_reciever.get_weather_for_all_places():
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=weather_text,
            parse_mode=ParseMode.MARKDOWN
        )


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Не знаю такой команды, котик("
    )


@hydra.main(config_path="configs", config_name="bot")
def run_bot(cfg: DictConfig) -> None:
    # bot base
    updater = Updater(token=cfg.bot.token, use_context=True)
    dispatcher = updater.dispatcher
    
    # weather reciever
    global weather_reciever
    weather_reciever = WeatherReciever(cfg.weather)

    # /start
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    # /weather
    weather_handler = CommandHandler("weather", weather)
    dispatcher.add_handler(weather_handler)

    # unknown commands
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # run the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    run_bot()
