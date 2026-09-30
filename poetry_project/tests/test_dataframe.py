import pandas as pd
import pytest

from plt_temp import build_dataframe


def test_build_dataframe_columns():
    hours = ["2026-09-30 00:00", "2026-09-30 01:00"]
    temps = [5.8, 5.1]
    df = build_dataframe(hours, temps)
    assert df.columns.tolist() == ["time", "temperature_c"]


def test_build_dataframe_row_count():
    hours = [f"2026-09-30 {h:02d}:00" for h in range(24)]
    temps = list(range(24))
    df = build_dataframe(hours, temps)
    assert len(df) == 24


def test_build_dataframe_sorted_by_time():
    hours = ["2026-09-30 05:00", "2026-09-30 03:00", "2026-09-30 04:00"]
    temps = [50, 30, 40]
    df = build_dataframe(hours, temps)
    times = df["time"].tolist()
    assert times == sorted(times)


def test_build_dataframe_temps_match_time():
    hours = ["2026-09-30 05:00", "2026-09-30 03:00", "2026-09-30 04:00"]
    temps = [50, 30, 40]
    df = build_dataframe(hours, temps)
    result = dict(zip(df["time"].astype(str), df["temperature_c"]))
    assert result["2026-09-30 03:00:00"] == 30
    assert result["2026-09-30 04:00:00"] == 40
    assert result["2026-09-30 05:00:00"] == 50
