import sys
from pathlib import Path
from time import sleep
from typing import List

import yaml

from .code import Screenshotter, crop


def is_logged_in(driver, base_url):
    driver.get(base_url)
    sleep(3)
    if base_url not in driver.current_url:
        return False
    else:
        return True


def run(filename: str):
    p = Path(filename)

    if not p.exists():
        raise ValueError("config file does not exist")

    y = yaml.safe_load(p.read_text())
    # print(y)
    print(f"screenshotz: loading file from {p.resolve()}")

    base_url = y["base_url"]
    page_width = y.get("page_width", None)
    s = Screenshotter(base_url, "cookies.cookies")

    driver = s.driver

    if page_width:
        driver.set_window_size(page_width, 768)

    if is_logged_in(driver, base_url):
        print("Already logged in")

        for page in y["pages"]:
            print("taking screenshot for page:")
            print(page)
            path = page.get("path", "/")
            driver.get(base_url + path)
            delay = page.get("delay", 1)

            sleep(delay)

            fname = page.get("out")

            fullscreen_name = "screenshots/" + fname + ".fullscreen.png"

            s.do_shot(fullscreen_name)

            crops = [page.get(x, 0) for x in "top bottom left right".split()]
            crop(fullscreen_name, "screenshots/" + fname, *crops)

    else:
        print("Not logged in. Please log in.")

        try:
            sleep(300)
        except KeyboardInterrupt:
            print("saving cookies and quitting...")
    s.quit()


def do_command() -> None:  # pragma: no cover
    try:
        args = parse_args(sys.argv[1:])
        run(args)
    except ValueError:
        print("Invalid args, please specify exactly two numbers")
        status = 1
    else:
        status = 0
    sys.exit(status)


def parse_args(args: List[str]) -> str:
    if args:
        return args[0]
    else:
        print("Error:You must spcify a config file.")
        raise ValueError
