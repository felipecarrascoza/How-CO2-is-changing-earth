#!/usr/bin/env python3
"""Baixa as séries instrumentais e gera site/data.js.

Fontes baixadas (GitHub datasets, espelhos dos dados oficiais):
  - NOAA GCAG: temperatura global anual (1850-hoje)
  - NOAA Mauna Loa: CO2 atmosférico anual (1959-hoje)
  - CDIAC/GCP: emissões fósseis globais (1750-hoje)
Fontes curadas à mão (aproximações, veja data/*.csv):
  - Temperatura 0-1849 (reconstruções tipo PAGES 2k)
  - CO2 0-1958 (testemunhos de gelo, tipo Law Dome)
"""
import csv, io, json, statistics, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = "https://raw.githubusercontent.com/datasets"


def fetch(path):
    with urllib.request.urlopen(f"{RAW}/{path}", timeout=60) as r:
        return list(csv.DictReader(io.StringIO(r.read().decode())))


def local(name):
    with open(ROOT / "data" / name) as f:
        return list(csv.DictReader(f))


temp_rows = [r for r in fetch("global-temp/main/data/annual.csv") if r["Source"] == "GCAG"]
temp = {int(r["Year"]): float(r["Mean"]) for r in temp_rows}
base = statistics.mean(v for y, v in temp.items() if 1850 <= y <= 1900)
temp = {y: round(v - base, 3) for y, v in temp.items()}  # anomalia vs 1850-1900

co2_mlo = {int(r["Year"]): float(r["Mean"]) for r in fetch("co2-ppm/main/data/co2-annmean-mlo.csv")}
emis = {
    int(r["Year"]): round(float(r["Total"]) * 3.664 / 1000, 3)  # MtC -> GtCO2
    for r in fetch("co2-fossil-global/main/data/global.csv")
}

data = {
    "temp_paleo": [[int(r["year"]), float(r["anomaly_c"])] for r in local("paleo_temperature_approx.csv")],
    "temp_instr": sorted(temp.items()),
    "co2_ice": [[int(r["year"]), float(r["ppm"])] for r in local("paleo_co2_approx.csv")],
    "co2_mlo": sorted(co2_mlo.items()),
    "emissions": sorted(emis.items()),
}
out = ROOT / "site" / "data.js"
out.write_text("window.DATA = " + json.dumps(data, separators=(",", ":")) + ";\n")
print("ok:", out, {k: len(v) for k, v in data.items()}, "baseline", round(base, 3))
