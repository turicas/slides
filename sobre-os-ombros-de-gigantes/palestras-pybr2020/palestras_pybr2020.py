import csv
import gzip
import io
import json
from functools import lru_cache
from pathlib import Path
from unicodedata import normalize
from urllib.parse import urlencode
from urllib.request import urlopen, Request


BASE_PATH = Path(__file__).parent
DATA_PATH = BASE_PATH / "data"
CALENDAR_EMAIL = "cis4uq8vegrfbjjn1qi9hvau1k@group.calendar.google.com"
CALENDAR_KEY = "AIzaSyAIn8DyZFtthupLozgwIX3NUURFMWEIPb4"
NAMES_URL = "https://data.brasil.io/dataset/genero-nomes/nomes.csv.gz"


@lru_cache()
def encode(name):
    ascii_name = normalize("NFKD", name).encode("ascii", errors="ignore").decode("ascii")
    return ascii_name.upper()


@lru_cache()
def load_name_data():
    filename = DATA_PATH / "nomes.csv.gz"

    # Download dataset file if it doesn't exist locally
    if not filename.exists():
        request = Request(NAMES_URL, headers={"User-Agent": "python-urllib"})
        response = urlopen(request)
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)
        with filename.open(mode="wb") as fobj:
            fobj.write(response.read())

    fobj = io.TextIOWrapper(gzip.open(str(filename.absolute())), encoding="utf-8")
    csv_reader = csv.DictReader(fobj)
    data = {
        row["first_name"]: row["classification"]
        for row in csv_reader
    }
    fobj.close()
    return data


def classify_name(name):
    name_data = load_name_data()
    encoded_name = encode(name)
    return name_data.get(encoded_name, None)


def calendar_items():
    base_url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_EMAIL}/events"
    query_string = {
        "key": CALENDAR_KEY,
        "timeMin": "2020-11-01T00:00:00.000Z",
        "timeMax": "2020-11-07T00:00:00.000Z",
        "singleEvents": "true",
        "maxResults": "9999",
        "timeZone": "America/Sao_Paulo",
    }
    response = urlopen(base_url + "?" + urlencode(query_string))
    data = json.loads(response.read())
    for item in data["items"]:
        full_name = item["extendedProperties"]["private"]["author"].strip()
        start_datetime = item["start"]["dateTime"]
        end_datetime = item["end"]["dateTime"]
        title = item["summary"]
        if full_name:
            first_name = full_name.split()[0]
            gender = classify_name(first_name)
        else:
            gender = ""

        yield {
            "full_name": full_name,
            "title": title,
            "gender": gender,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
        }


if __name__ == "__main__":
    output_filename = DATA_PATH / "palestras-pybr2020.csv"
    with open(output_filename, mode="w") as fobj:
        writer = None
        for item in calendar_items():
            if writer is None:
                writer = csv.DictWriter(fobj, fieldnames=list(item.keys()))
                writer.writeheader()
            writer.writerow(item)
