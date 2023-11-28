import requests
import telebot
import yaml


with open('images.yaml') as f:
    IMAGES = yaml.safe_load(f)


with open('token.yaml') as f:
    TOKENS = yaml.safe_load(f)


TOKEN_TELEGRAM = TOKENS['token_telegram']
TOKEN_BRAWL_START_API = TOKENS['token_brawl_start_api']
HEADERS = {"Authorization": f"Bearer {TOKEN_BRAWL_START_API}"}

bot = telebot.TeleBot(TOKEN_TELEGRAM)

def extract_arg(arg):
    return arg.split()[1:]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGPwABY12NOKH83l70SWaLWdHgvC6M8TQAAqkAA8O54TBZeMcJ591vLSoE')
    bot.send_message(message.chat.id, 'Я еще в разработке! Но скоро ты увидишь меня во всей красе')


def get_player_brawler_stat(player_tag: str, brawler_name: str, headers: dict) -> tuple:
    """
    Функция возвращает статистику игрока по конкретному бравлеру
    :param player_tag: таг игрока
    :param brawler_name: имя бравлера
    :param headers: хэдэрсы для запроса
    :return:
    """
    url = 'https://api.brawlstars.com/v1/players/%23' + player_tag
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        brawlers = response.json()['brawlers']
        for brawler in brawlers:
            if brawler.get('name') == brawler_name:
                rank = brawler['rank']
                trophies = brawler['trophies']
                return rank, trophies

def the_best_player():
