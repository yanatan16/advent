import os
from pathlib import Path
import httpx
import sys
import datetime
import zoneinfo

def get_input(year: int, day: int) -> str:
    fn = Path(__file__).parent.parent.parent / f'.inputs/{year}/{day}.txt'
    try:
        with fn.open('r') as f:
            return f.read()
    except FileNotFoundError:
        session_cookie = os.environ['ADVENT_SESSION_COOKIE']
        with httpx.Client() as client:
            resp = client.get(f'https://adventofcode.com/{year}/day/{day}/input', headers={'Cookie': f'session={session_cookie}'})

            if resp.status_code == 404:
                release = datetime.datetime(2024, 12, 6, tzinfo=zoneinfo.ZoneInfo("America/New_York"))
                now = datetime.datetime.now(zoneinfo.ZoneInfo("UTC"))
                time_to_release = release - now
                print(f"{year} Day {day} hasn't started yet, it comes out midnight EST on December {day}, which {time_to_release} away")
                sys.exit(1)

            resp.raise_for_status()

            body = resp.text

            fn.parent.mkdir(parents=True, exist_ok=True)
            with fn.open('w') as f:
                f.write(body)

            return body
