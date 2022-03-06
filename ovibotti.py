import logging
import time
import datetime
import pytz

from telegram import Update
from telegram.ext import  Updater, CommandHandler, CallbackContext

statuskey = "status_key"
timekey = "time_key"
DOOR_STATUS = "Tuntematon"



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """käynnistää botin ja ajastetut toiminnot."""
    update.message.reply_text('testi')
    DOOR_STATUS = "Tuntematon"
    action_time = time.strftime("%d.%m.%Y klo %H:%M:%S", time.localtime())
    context.chat_data[statuskey] = DOOR_STATUS
    context.chat_data[timekey] = action_time

"""
    context.job_queue.run_daily(unlock_door, datetime.time(hour=13, minute=39,
                tzinfo=pytz.timezone('Europe/Helsinki')), days=(0, 1, 2, 3, 4),
                                context=context)
"""


def door_reminder(update: Update, context: CallbackContext):
    """Lähettää muistutusviestin. Kutsutaan vain jos tarve"""
    print("Killan ovi on vielä auki")


def lock_door(update: Update, context: CallbackContext):
    """Vaihtaa oven statuksen aukinaisesta lukituksi. Palauttaa viestissä
     oven lukitsijan sekä toki kiitoksen"""
    #update.message.reply_sticker("CAADAgADHgEAAiHfMQE_pcz3yBGAdwI")
    action_time = time.strftime("%d.%m.%Y klo %H:%M:%S", time.localtime())
    context.chat_data[statuskey] = "Lukittu"
    context.chat_data[timekey] = action_time
    print("Ovi lukittu", action_time)
    reply = "Ovi lukittu " + str(action_time)
    update.message.reply_text(reply)


def unlock_door(update: Update, context: CallbackContext):
    """Vaihtaa oven statuksen aukinaiseksi. Ei anna palautetta, koska tarkoitus
    kutsua automaattisesti."""

    action_time = time.strftime("%d.%m.%Y klo %H:%M:%S", time.localtime())
    context.chat_data[statuskey] = "Avattu"
    context.chat_data[timekey] = action_time




def get_status(update: Update, context: CallbackContext):
    """Kertoo onko ovi lukossa vai auki ja sen milloin tieto on päivitetty"""
    DOOR_STATUS = context.chat_data.get(statuskey)
    action_time = context.chat_data.get(timekey)
    try:
        reply = str(DOOR_STATUS + " " + str(action_time))
    except:
        reply = str("Tuntematon")
    print(reply)
    update.message.reply_text(reply)


def main() -> None:
    """Käynnistää pollaamisen, oven tila tuntematon kun botti käynnistetty.
    Tallentaa myös ajan jolloin botti on käynnistetty"""
    updater = Updater('TOKEN')
    print("kissa, oven tila tuntematon")


    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    """data = dispatcher.chat_data[]
    job_cue = dispatcher.job_queue.run_daily(unlock_door, datetime.time(hour=11, minute=47,
                tzinfo=pytz.timezone('Europe/Helsinki')), days=(0, 1, 2, 3, 4),
                                   context=data)
"""


    dispatcher.add_handler(CommandHandler("start", start, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler("reminder", door_reminder, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler("lock_door", lock_door, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler("unlock_door", unlock_door, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler("status", get_status, pass_job_queue=True))

    updater.start_polling()


if __name__ == '__main__':
    main()
