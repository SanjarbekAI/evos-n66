from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.i18n import I18n

from core.config import LOCALES_DIR, I18N_DOMAIN, TOKEN

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

i18n = I18n(path=LOCALES_DIR, default_locale="en", domain=I18N_DOMAIN)
_ = i18n.gettext
