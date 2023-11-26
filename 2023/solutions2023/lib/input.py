import os
from pathlib import Path
import httpx

def get_input(year: int, day: int) -> str:
    fn = Path(__file__).parent.parent.parent / f'.inputs/{year}/{day}.txt'
    try:
        with fn.open('r') as f:
            return f.read()
    except FileNotFoundError:
        session_cookie = os.environ['ADVENT_SESSION_COOKIE']
        with httpx.Client() as client:
            resp = client.get(f'https://adventofcode.com/{year}/day/{day}/input', headers={'Cookie': f'session={session_cookie}'})
            resp.raise_for_status()

            body = resp.text

            fn.parent.mkdir(parents=True, exist_ok=True)
            with fn.open('w') as f:
                f.write(body)

            return body
