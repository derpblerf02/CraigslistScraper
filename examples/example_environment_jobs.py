import craigslistscraper as cs
import re

ENV_KEYWORDS = [
    "environment",
    "sustain",
    "sustainable",
    "green",
    "renewable",
    "climate",
    "eco",
    "environmental",
]

MIN_PAY = 3000
MAX_PAY = 12500


def contains_environment_keywords(text: str) -> bool:
    lower = text.lower()
    return any(keyword in lower for keyword in ENV_KEYWORDS)


def parse_pay(text: str):
    match = re.search(r"\$([\d,]+)(?:\s*[-to]+\s*\$([\d,]+))?", text)
    if match:
        amount = match.group(1)
        return float(amount.replace(",", ""))
    return None


def filter_environment_ads(ads):
    good = []
    for ad in ads:
        status = ad.fetch()
        if status != 200:
            continue
        text = f"{ad.title or ''} {ad.description or ''}"
        if not contains_environment_keywords(text):
            continue
        pay = parse_pay(text)
        if pay is None or not (MIN_PAY <= pay <= MAX_PAY):
            continue
        good.append({
            "title": ad.title,
            "url": ad.url,
            "pay": pay,
        })
    return good


if __name__ == "__main__":
    search = cs.Search(
        query="environment",
        city="seattle",
        category="sof",
    )
    status = search.fetch()
    if status != 200:
        raise SystemExit(f"Unable to fetch search with status <{status}>")
    env_ads = filter_environment_ads(search.ads)
    print(f"{len(env_ads)} environment-friendly ads found!")
    for ad in env_ads:
        print(ad)
