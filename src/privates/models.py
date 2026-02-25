from typing import Sequence
import pandas as pd


def takahashi_alexander(
    cc: float = 1_000_000,
    rc: Sequence[float] = [0.29] + [0.3] * 19,
    b: float = 1.2,
    g: float | Sequence[float] = 0.2,
    y: float = 0.0,
    nav: float = 0.0,
    age: int = 0,
    pic: float = 0.0,
) -> pd.DataFrame:
    if isinstance(g, Sequence):
        assert len(g) == len(rc)
    else:
        g = [g] * len(rc)
    df = pd.DataFrame(index=pd.RangeIndex(1, len(rc) + 1, name="Period"))
    df.index += age
    df["G"] = g
    df["RC"] = rc
    df["RD"] = (df.index / (len(rc) + age)) ** b
    df["RD"] = df["RD"].apply(lambda cell: max(y, cell))
    df["PIC"] = pic
    df["NAV"] = nav
    for idx, row in df.iterrows():
        assert isinstance(idx, int)
        df.loc[idx, "Capital Call"] = df.loc[idx, "RC"] * (cc - df.loc[idx, "PIC"])
        if idx < (len(rc) + age):
            df.loc[idx + 1, "PIC"] = df.loc[idx, "PIC"] + df.loc[idx, "Capital Call"]
        df.loc[idx, "Distribution"] = (
            (df.loc[idx, "NAV"] if idx == (age + 1) else df.loc[idx - 1, "NAV"])
            * (1 + df.loc[idx, "G"])
            * row["RD"]
        )
        df.loc[idx, "NAV"] = (
            (df.loc[idx, "NAV"] if idx == (age + 1) else df.loc[idx - 1, "NAV"])
            * (1 + df.loc[idx, "G"])
            + df.loc[idx, "Capital Call"]
            - df.loc[idx, "Distribution"]
        )
    return df[["NAV", "Capital Call", "Distribution"]].astype(float)
