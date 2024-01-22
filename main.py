from bot import mybot
from utils import TOKEN

if __name__ == "__main__":
    try:
        mybot.run(token=TOKEN)
    except Exception as e:
        print(e)