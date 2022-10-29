from pprint import pprint

import requests
from bs4 import BeautifulSoup
from match import Match
import datetime


def fetch_card_data():
    date = ""
    card_name = ""
    link = ""

    soup = BeautifulSoup(requests.get("https://www.espn.com/mma/schedule").content, "html.parser")

    for ele in soup.find_all("tr"):
        if ele.has_attr("class") and "Table__TR--sm" in ele["class"]:
            try:
                date = ele.find("span").contents[0]
                date = date + " " + ele.find('a').contents[0]
                for sub_ele in ele.find_all("a", href=True):
                    if "/mma/fightcenter/_/id" in sub_ele["href"] and "PM" not in sub_ele.contents[0]:
                        card_name = sub_ele.contents[0]
                        link = sub_ele["href"]
                break
            except AttributeError:
                pass

    card_data = {"name": card_name,
                 "date": f'**{date}**',
                 "matches": []}

    schedule_soup = BeautifulSoup(requests.get(f"https://www.espn.com{link}").content, "html.parser")

    all_odds = []
    for d in schedule_soup.find_all("div"):
        if d.has_attr("class") and "ScoreCell__Odds" in d["class"]:
            all_odds.append(d.contents[0])
            all_odds.append(d.contents[0])

    fighters = []
    order = 1
    for d in schedule_soup.find_all("div"):
        if d.has_attr("class") and "MMACompetitor" in d["class"]:
            name = d.find("span").contents[0]
            record = "None"
            for r in d.find_all("div"):
                if r.has_attr("class") and "n9" in r["class"]:
                    for s in r.contents:
                        if "-" in s:
                            record = s
            if len(all_odds) != 0:
                odds = all_odds[0]
                all_odds.remove(odds)
            else:
                odds = "None"
            fighters.append([name, odds, record])
            if len(fighters) == 2:
                card_data["matches"].append(Match(fighters[0], fighters[1], order))
                order += 1
                fighters = []

    return card_data

print(fetch_card_data())
