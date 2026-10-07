#!/usr/bin/env python3
"""One-shot, low-rate VarAtlas province aggregation for Hacettepe programs.

Only public university/detail pages and the public per-program JSON payload are
used. Raw payloads stay in the ignored cache directory and are never copied to
the dashboard output.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "https://varatlas.com"
DATA_BASE = "https://data.varatlas.com/jsons_merged"
UNIVERSITY_URL = f"{BASE}/universite/HACETTEPE%20%C3%9CN%C4%B0VERS%C4%B0TES%C4%B0"
PROVINCES = (
    "ADANA ADIYAMAN AFYONKARAHİSAR AĞRI AKSARAY AMASYA ANKARA ANTALYA ARDAHAN "
    "ARTVİN AYDIN BALIKESİR BARTIN BATMAN BAYBURT BİLECİK BİNGÖL BİTLİS BOLU "
    "BURDUR BURSA ÇANAKKALE ÇANKIRI ÇORUM DENİZLİ DİYARBAKIR DÜZCE EDİRNE "
    "ELAZIĞ ERZİNCAN ERZURUM ESKİŞEHİR GAZİANTEP GİRESUN GÜMÜŞHANE HAKKARİ "
    "HATAY IĞDIR ISPARTA İSTANBUL İZMİR KAHRAMANMARAŞ KARABÜK KARAMAN KARS "
    "KASTAMONU KAYSERİ KİLİS KIRIKKALE KIRKLARELİ KIRŞEHİR KOCAELİ KONYA "
    "KÜTAHYA MALATYA MANİSA MARDİN MERSİN MUĞLA MUŞ NEVŞEHİR NİĞDE ORDU "
    "OSMANİYE RİZE SAKARYA SAMSUN SİİRT SİNOP SİVAS ŞANLIURFA ŞIRNAK "
    "TEKİRDAĞ TOKAT TRABZON TUNCELİ UŞAK VAN YALOVA YOZGAT ZONGULDAK"
).split()
PROVINCE_RE = re.compile(
    r"(?<![A-ZÇĞİÖŞÜ])(" + "|".join(map(re.escape, sorted(PROVINCES, key=len, reverse=True))) + r")(?![A-ZÇĞİÖŞÜ])"
)


class NoProvinceData(ValueError):
    """A public program payload exists but has no Turkish province rows."""


def fetch(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "hacettepe-data-viz/1.0 public-data-import"})
    with urlopen(request, timeout=30) as response:
        return response.read()


def discover_program_ids(html: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for slug, program_id in re.findall(r"/detay/([^\"'<> ]+?)-(\d{9})", html):
        found[program_id] = f"{BASE}/detay/{slug}-{program_id}"
    return found


def province_from_school(value: str) -> str | None:
    match = PROVINCE_RE.search(value.upper().replace("İ", "İ"))
    return match.group(1) if match else None


def aggregate(payload: dict, year: str) -> tuple[dict[str, int], int]:
    if str(payload.get("yil", "")) != year:
        raise ValueError(f"payload yılı {payload.get('yil')!r}, beklenen {year}")
    rows = payload.get("lise_bazinda_yerlesen_json")
    if not isinstance(rows, list):
        raise NoProvinceData("lise_bazinda_yerlesen_json bulunamadı")
    totals: dict[str, int] = defaultdict(int)
    for row in rows:
        school = str(row.get("Lise", ""))
        count = row.get("Toplam")
        if not school or count is None:
            continue
        province = province_from_school(school)
        if province:
            totals[province] += int(float(str(count).replace(",", ".")))
    if not totals:
        raise NoProvinceData("lise kayıtlarından il çıkarılamadı")
    return dict(totals), sum(totals.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", default="2025")
    parser.add_argument("--delay", type=float, default=1.0, help="seconds between uncached detail requests")
    parser.add_argument("--cache-dir", type=Path, default=Path("data/varatlas-cache"))
    parser.add_argument("--output", type=Path, default=Path("data/varatlas-2025-il.csv"))
    args = parser.parse_args()
    if args.delay < 0.5:
        parser.error("--delay must be at least 0.5 seconds")

    args.cache_dir.mkdir(parents=True, exist_ok=True)
    try:
        html = fetch(UNIVERSITY_URL).decode("utf-8", errors="replace")
    except (HTTPError, URLError, TimeoutError) as error:
        print(f"ERROR university page: {error}", file=sys.stderr)
        return 1
    programs = discover_program_ids(html)
    if not programs:
        print("ERROR no public Hacettepe program IDs found", file=sys.stderr)
        return 1
    totals: dict[str, int] = defaultdict(int)
    failures: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    fetched = date.today().isoformat()
    for index, program_id in enumerate(sorted(programs), start=1):
        cache = args.cache_dir / f"{program_id}.json"
        url = f"{DATA_BASE}/{program_id}.json"
        try:
            if cache.exists():
                payload = json.loads(cache.read_text(encoding="utf-8"))
            else:
                if index > 1:
                    time.sleep(args.delay)
                payload = json.loads(fetch(url).decode("utf-8"))
                cache.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            program_totals, _ = aggregate(payload, args.year)
            for province, count in program_totals.items():
                totals[province] += count
        except NoProvinceData as error:
            skipped.append({"program_id": program_id, "url": programs[program_id], "reason": str(error)})
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ValueError, KeyError) as error:
            failures.append({"program_id": program_id, "url": url, "error": str(error)})
        print(f"[{index}/{len(programs)}] {program_id}", file=sys.stderr)

    report = args.cache_dir / "report.json"
    report.write_text(json.dumps({"failed": failures, "skipped_no_province_data": skipped}, ensure_ascii=False, indent=2), encoding="utf-8")
    if failures:
        print(f"ERROR {len(failures)} program(s) failed; see {report}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["il", "ogrenci_sayisi", "yil", "kaynak"])
        for province in sorted(totals):
            writer.writerow([province, totals[province], args.year, f"VarAtlas program payloadları, erişim {fetched}"])
    if skipped:
        print(f"WARNING {len(skipped)} programs had no public Turkish province rows; see {report}", file=sys.stderr)
    print(f"Wrote {len(totals)} provinces from {len(programs) - len(skipped)} programs to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
