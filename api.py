from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from PIL import Image
from io import BytesIO

SOURCE_URL = "https://poweron.loe.lviv.ua/"

def get_image_url() -> str:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(SOURCE_URL)

    driver.implicitly_wait(10)

    image_element = driver.find_element(By.XPATH, "//img[@alt='grafic']")
    image_url = image_element.get_attribute("src")

    return image_url

def get_image_by_url(url: str) -> Image:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        image = Image.open(BytesIO(res.content))
        return image

    else:
        print(res.status_code)

def get_schedule_from_image(image: Image) -> list[list[bool]]:
    pixels = {
        (150, 201, 61, 255): True,
        (255, 113, 23, 255): False
    }

    start_x, start_y = 96, 188
    end_x, end_y = 1450, 430
    offset_x, offset_y = 58, 43

    found_pixels = set()
    schedule = [[False for time in range(24)] for group in range(6)]

    for y_idx, y in enumerate(range(start_y, end_y, offset_y)):
        for x_idx, x in enumerate(range(start_x, end_x, offset_x)):
            schedule[y_idx][x_idx] = pixels[image.getpixel((x, y))]

    return schedule

def get_schedule_for_group(schedule: list[list[bool]], group: str) -> list[bool]:
    groups = {
        '1.1': 0,
        '1.2': 1,
        '2.1': 2,
        '2.2': 3,
        '3.1': 4,
        '3.2': 5,
    }

    possible_off = []

    for idx, is_light in enumerate(schedule[groups[group]]):
        if not is_light:
            possible_off.append(idx)

    return schedule[groups[group]], possible_off

def process_possible_off(possible_off: list[int]) -> list[tuple[int, int]]:
    if not possible_off:
        return []

    results = []

    off_start = possible_off[0]
    last_hour = 0

    for idx, hour in enumerate(possible_off):
        if hour - last_hour > 1:
            results.append((off_start, last_hour + 1))
            off_start = hour

        last_hour = hour

        if idx == len(possible_off) - 1:
            results.append((off_start, hour + 1))

    return results

GROUP = '1.1'

def get_offs_timelines():
    image_url = get_image_url()
    image = get_image_by_url(image_url)

    schedule = get_schedule_from_image(image)
    group_schedule, possible_off = get_schedule_for_group(schedule, GROUP)
    offs_timelines = process_possible_off(possible_off)
    return offs_timelines

if __name__ == "__main__":
    image_url = get_image_url()
    image = get_image_by_url(image_url)

    schedule = get_schedule_from_image(image)
    # schedule = get_schedule_from_image(Image.open('fetched_grafic.png'))
    group_schedule, possible_off = get_schedule_for_group(schedule, GROUP)
    offs_timelines = process_possible_off(possible_off)
    print(offs_timelines)
