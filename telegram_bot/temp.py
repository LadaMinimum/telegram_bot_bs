import requests
import yaml
from pprint import pprint


with open('token.yaml') as f:
    yaml_dict = yaml.safe_load(f)


TOKEN_TELEGRAM = yaml_dict['token_telegram']
TOKEN_BRAWL_START_API = yaml_dict['token_brawl_start_api']
HEADERS = {"Authorization": f"Bearer {TOKEN_BRAWL_START_API}"}


# brawler_name = 'SHELLY'
# player_tag = 'YQ802RC29'
# url = 'https://api.brawlstars.com/v1/players/%23' + player_tag
# print(url)
# response = requests.get(url, headers=HEADERS).json()
# print(response)
# brawlers = response['brawlers']
# for brawler in brawlers:
#     if brawler.get('name') == brawler_name:
#         rank = brawler['rank']
#         trophies = brawler['trophies']
# print(f' Ранг бойца: {rank}, Количество кубков = {trophies}')


# def comparison(player_tag):
# player_tag = 'YQ802RC29'
# player_tag2 = 'PLL2LVCRQ'
# url_player = 'https://api.brawlstars.com/v1/players/%23' + player_tag2
# url_global = 'https://api.brawlstars.com/v1/rankings/global/players'
# resp_global = requests.get(url_global, headers=HEADERS).json()
# for key, value in resp_global.items():
#     # print(value)
#     for count, player in enumerate(value):
#         if count < 1:
#             print(player)
#             for k, v in player.items():
#                 best = player['trophies']
#                 # print(best)
#     break
# resp_player = requests.get(url_player, headers=HEADERS).json()
# print(resp_player)
# for k, v in resp_player.items():
#    my_trophies = resp_player['trophies']
#    # print(my_trophies)
# the_comparison = int(best) - int(my_trophies)
# print(the_comparison)


player_tag = 'YQ802RC29'
url = 'https://api.brawlstars.com/v1/players/%23' + player_tag +'/battlelog'
print(url)
battle_result = []
translate = {'defeat': "поражение", 'victory': "победа", 'draw': "ничья"}
req = requests.get(url, headers=HEADERS).json()
for key, value in req.items():
    if key == 'items':
        # print(key, value)
        for i in value:
            print(i)
            try:
                battle_result.append(i["battle"]['result'])
            except:
                continue
            print(battle_result)
        defeats = 0
        for counts in battle_result:
            if counts in 'defeat':
                defeats += 1
        percent_of_defeats = defeats * 4
        percent_of_victories = (25 - defeats) * 4
        print(f'Процент проигрышей за последние 25 боев составляет: {percent_of_defeats} %, "\n" Процент побед за последние 25 боев соствляет: {percent_of_victories} %')
        tr = ''
        for words in battle_result:
            if words in translate:
                tr += translate.get(words) + '\n'
        print(tr)

        print(battle_result)

