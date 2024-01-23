from bot import mybot, logger
from utils import TOKEN


if __name__ == "__main__":
    logger.info("Script started")
    try:
        mybot.run(token=TOKEN)
    except Exception as e:
        logger.error("Exception occurred", exc_info=True, stack_info=True)
        print(e)
    logger.critical("Bot stopped running")