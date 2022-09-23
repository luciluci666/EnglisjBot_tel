import logging
from aiogram import Bot, Dispatcher
from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter
import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import tzlocal



# Configure logging
logging.basicConfig(level=logging.INFO)

# prerequisites
if not config.BOT_TOKEN:
    exit("No token provided")

# init
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# activate filters
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)

# activate sheduler
scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))

