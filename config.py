from environs import Env
import loguru

logger = loguru.logger
logger.add('Logs/bot_log.log', format='{time} {level} {message}', rotation='512 KB', compression='zip')

env = Env()
env.read_env()

telegram_token = env.str("TELEGRAM_TOKEN")
telegram_admin_id = env.int("TELEGRAM_ADMIN_ID")

debug = env.bool("DEBUG")
