import io
import zipfile

import requests
import pandas as pd

YEAR = 2023


def get_ipeds_admissions(year: int) -> pd.DataFrame:
    url = f"https://nces.ed.gov/ipeds/datacenter/data/ADM{year}.zip"
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    csv_name = [f for f in z.namelist() if f.endswith(".csv")][0]
    with z.open(csv_name) as f:
        df = pd.read_csv(f, encoding="latin1")
        df.to_csv("data.csv", index=False)
    return df


def get_institutions(year: int) -> pd.DataFrame:
    url = f"https://nces.ed.gov/ipeds/datacenter/data/HD{year}.zip"
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    csv_name = [f for f in z.namelist() if f.endswith(".csv")][0]
    with z.open(csv_name) as f:
        df = pd.read_csv(f)
        df.to_csv("data.csv", index=False)
    return df
