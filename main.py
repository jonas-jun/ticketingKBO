import requests
from sconf import Config
from utils import str_from_timestamp, get_today
import pandas as pd


def get_sources(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"failure: {response.status_code}")
        return None


def main(cfg: Config):
    url = cfg.url
    headers = cfg.headers
    sources = get_sources(url, headers)
    result = list()
    for game in sources["data"]:
        scheduleId = str(game["scheduleId"])
        productId = str(game["productId"])
        title = game["matchTitle"]
        homeTeam = game["homeTeam"]["teamName"]
        awayTeam = game["awayTeam"]["teamName"]
        field = game["venueName"]
        schedule = str_from_timestamp(game["scheduleDate"])
        openTime = str_from_timestamp(game["reserveOpenDateTime"])
        link = f"https://www.ticketlink.co.kr/reserve/product/{productId}?scheduleId={scheduleId}"
        result.append(
            {
                "date": schedule,
                "home_team": homeTeam,
                "away_team": awayTeam,
                "field": field,
                "open_time": openTime,
                "link": link,
                "game_title": title,
                "schedule_id": scheduleId,
                "product_id": productId,
            }
        )
    result = sorted(result, key=lambda x: x["date"])
    df = pd.DataFrame(result)
    out_f = f"schedules_{cfg.platform}_{get_today("%y-%m-%d")}.xlsx"
    df.to_excel(out_f, index=False)
    print(f"{out_f} exported!")


if __name__ == "__main__":
    cfg = "config_ticketlink.yaml"
    cfg = Config(cfg)
    main(cfg)
