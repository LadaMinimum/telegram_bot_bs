import requests
import telebot
import yaml


#with open('images.yaml') as f:
#    IMAGES = yaml.safe_load(f)


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
    else:
        raise requests.exceptions.RequestException(
            f'ERROR! Status code: {response.status_code}, text: {response.text}'
        )


# @bot.message_handler(commands=['get_player_brawler_stat'])
# def main(message):
#     args = extract_arg(message.text)
#     rank, trophies = get_player_brawler_stat(args[0], args[1], HEADERS)
#     try:
#         with open(f'images/{args[1]}.jpg', 'rb') as f:
#             pic = f.read()
#             bot.send_photo(message.chat.id, photo=pic)
#     except FileNotFoundError as e:
#         bot.send_message(message.chat.id, 'Картинка не найдена, сорян!')
#     bot.reply_to(message, f'Rank: {rank} / Trophies: {trophies}')
list_of_images_brawlers = ['SHELLY', 'COLT', 'BO', 'CORDELIUS', 'BROCK', 'BEA', 'DYNAMIKE', 'CROW']

@bot.message_handler(commands=['get_player_brawler_stat'])
def main(message):
    args = extract_arg(message.text)
    print(args)
    if args[1] in list_of_images_brawlers:
        with open(f'images/{args[1]}.jpg', 'rb') as f:
            pic = f.read()
            bot.send_photo(message.chat.id, photo=pic)
    rank, trophies = get_player_brawler_stat(args[0], args[1], HEADERS)
    # bot.send_photo(message.chat.id, photo=IMAGES[args[1]])
    bot.reply_to(message, f'Rank: {rank} / Trophies: {trophies}')




def comparison(player_tag):
    url_player = 'https://api.brawlstars.com/v1/players/%23' + player_tag
    url_global = 'https://api.brawlstars.com/v1/rankings/global/players'
    resp_global = requests.get(url_global, headers=HEADERS).json()
    for key, value in resp_global.items():
        # print(value)
        for count, player in enumerate(value):
            if count < 1:
                # print(player)
                for k, v in player.items():
                    best = player['trophies']
                    # print(best)
        break
    resp_player = requests.get(url_player, headers=HEADERS).json()
    print(resp_player)
    for k, v in resp_player.items():
       my_trophies = resp_player['trophies']
       # print(my_trophies)
    the_comparison = int(best) - int(my_trophies)
    return the_comparison

@bot.message_handler(commands=['the_comparison_with_best'])
def comp(message):
    args = extract_arg(message.text)
    print(args)
    the_comparison = comparison(args[0])
    bot.reply_to(message, f'Разница в трофеях с самым лучшим игроком мира равна: {the_comparison}')

def battle_results(player_tag):
    url = 'https://api.brawlstars.com/v1/players/%23' + player_tag + '/battlelog'
    battle_result = []
    translate = {'defeat': "поражение", 'victory': "победа", 'draw': "ничья"}
    req = requests.get(url, headers=HEADERS).json()
    for key, value in req.items():
        if key == 'items':
            # print(key, value)
            for i in value:
                # print(i)
                try:
                    battle_result.append(i["battle"]['result'])
                except:
                    continue
                # print(battle_result)
            defeats = 0
            for counts in battle_result:
                if counts in 'defeat':
                    defeats += 1
            percent_of_defeats = defeats * 4
            percent_of_victories = (25 - defeats) * 4
            percent = (
                f'Процент проигрышей за последние 25 боев составляет: {percent_of_defeats} %, "\n" Процент побед за последние 25 боев соствляет: {percent_of_victories} %')
            tr = ''
            for words in battle_result:
                if words in translate:
                    tr += translate.get(words) + '\n'
            tr += percent + '\n'
            return tr



@bot.message_handler(commands=['result'])
def result(message):
    args = extract_arg(message.text)
    print(args)
    res = battle_results(args[0])
    bot.reply_to(message, f'Результаты последних 25 боев: {res}')

bot.infinity_polling()

