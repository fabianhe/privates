import pandas as pd
import pyxirr
from pyxirr import pe
import numpy as np


def metrics(
    df: pd.DataFrame,
    cc: float = 1_000_000,
    nav: float = 0.0,
    pic: float = 0.0,
    distributions: float = 0.0,
) -> pd.Series:
    df_copy = df.copy().sort_index()
    df_copy["Net Cash Flow"] = df_copy["Distribution"] - df_copy["Capital Call"]
    df_copy["Net Cash Flow incl. NAV"] = df_copy["Net Cash Flow"]
    df_copy.loc[df_copy.index[-1], "Net Cash Flow incl. NAV"] += df_copy["NAV"].iloc[-1]

    results = pd.Series(name="Value").rename_axis("Metric")
    results["PIC"] = df_copy["Capital Call"].sum() + pic
    results["Capital Called (% Committed)"] = results["PIC"] / cc
    results["Distributions"] = df_copy["Distribution"].sum() + distributions
    results["NAV"] = df_copy["NAV"].iloc[-1]
    results["DPI"] = pe.dpi_2(
        [pic] + list(df_copy["Capital Call"]),
        [distributions] + list(df_copy["Distribution"]),
    )
    results["RVPI"] = pe.rvpi([pic] + list(df_copy["Capital Call"]), results["NAV"])
    results["TVPI"] = pe.tvpi_2(
        [pic] + list(df_copy["Capital Call"]),
        [distributions] + list(df_copy["Distribution"]),
        results["NAV"],
    )
    results["MOIC"] = pe.moic_2(
        [pic] + list(df_copy["Capital Call"]),
        [distributions] + list(df_copy["Distribution"]),
        results["NAV"],
    )

    results["IRR"] = pyxirr.irr(
        [-nav] + list(df_copy["Net Cash Flow incl. NAV"].values)
    )
    results["TWR"] = (
        np.exp(
            np.log(
                (df_copy["NAV"] + df_copy["Net Cash Flow"])
                .div(df_copy["NAV"].shift(1), axis=0)
                .mean()
            )
        )
        - 1
    )
    results["Duration"] = np.log(results["TVPI"]) / np.log(1 + results["IRR"])
    results["Duration Fraction"] = results["Duration"] / df_copy.index.max()
    results["Approximate Bow"] = np.exp(np.pi * results["Duration Fraction"]) / np.sqrt(
        2
    )
    return results
