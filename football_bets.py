import requests
from bs4 import BeautifulSoup
import re

LIGUES_ID = {
    "premier league": "46",
    "la liga": "16108",
    "bundesliga": "43",
    "seria a": "42"
}


#  r = requests.post('http://httpbin.org/post', data = {'key':'value'})
# https://sports.bwin.com/en/sports/indexmultileague
def get_ligue_parse_html(url):
    r = requests.post(url, data={'sportId': '4',
                                 'page': '0',
                                 'leagueIds': [LIGUES_ID.values()]
                                 })
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    return soup


def get_ligue_url(ligue):
    return LIGUES_ID.get(ligue)


x = "https://sports.bwin.com/en/sports/indexmultileague"
soup = get_ligue_parse_html(x)


# print(soup.prettify())

def re_stake(stake):
    stake_word = re.findall(r"([\d.]*\d+)", stake)
    return stake_word


def get_local_bets(soup):
    result = soup.find_all('div', {
        'class': "marketboard-event-group__item-container marketboard-event-group__item-container--level-2"})
    # print(len(result))
    bets = []
    for z in range(len(result)):
        bet_rows = result[z].find_all('tr', {'class': "marketboard-options-row marketboard-options-row--3-way"})
        # print(bet_rows)
        for row in bet_rows:
            choices = row.select('.mb-option-button__option-name')
            odds = row.select('.mb-option-button__option-odds')

            bet = {
                symbol: {
                    'team': choices[i].text,
                    'odds': odds[i].text,
                }
                for i, symbol in enumerate(['1', 'X', '2'])
                }
            bet['meta'] = {
                'hour': '12:00UTC',
                'day': '123231',
                'home': choices[0].text,
                'away': choices[2].text
            }

            bets.append(bet)
    print(bets)
    print(len(bets))


get_local_bets(soup)

#
# if __name__ == '__main__':
#     soup = get_ligue_parse_html(get_ligue_url("la liga"))
#     print(soup)
#     get_local_bets(soup)
