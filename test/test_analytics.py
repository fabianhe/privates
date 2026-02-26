from privates import analytics
from privates import models
import pandas as pd
import pandas.testing as pdt
import pytest

test_cases = [
    (
        {
            "cc": 1_000_000.00,
            "rc": [0.25, 1 / 3, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.0],
            "b": 2.3,
            "g": 0.15,
            "y": 0.0,
            "nav": 0.0,
            "age": 0,
            "pic": 0.0,
            "distributions": 0.0,
        },
        pd.Series(
            {
                "PIC": 1_000_000,
                "Capital Called (% Committed)": 1.0,
                "Distributions": 1_997_595.20,
                "NAV": 0.0,
                "DPI": 2.0,
                "RVPI": 0.0,
                "TVPI": 2.0,
                "MOIC": 2.0,
                "IRR": 0.15,
                "TWR": 0.15,
                "Duration": 4.95,
                "Duration Fraction": 0.413,
                "Approximate Bow": 2.585,
            },
            name="Value",
        ).rename_axis("Metric"),
    ),
    (
        {
            "cc": 1_000_000.00,
            "rc": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.0],
            "b": 2.3,
            "g": 0.15,
            "y": 0.0,
            "nav": 1_011_150.58,
            "age": 4,
            "pic": 875_000.0,
            "distributions": 106_898.53,
        },
        pd.Series(
            {
                "PIC": 1_000_000,
                "Capital Called (% Committed)": 1.0,
                "Distributions": 1_997_595.20,
                "NAV": 0.0,
                "DPI": 2.0,
                "RVPI": 0.0,
                "TVPI": 2.0,
                "MOIC": 2.0,
                "IRR": 0.15,
                "TWR": 0.15,
                "Duration": 4.95,
                "Duration Fraction": 0.413,
                "Approximate Bow": 2.585,
            },
            name="Value",
        ).rename_axis("Metric"),
    ),
]


@pytest.mark.parametrize("inputs, expected_df", test_cases)
def test_takahashi_alexander(inputs, expected_df):
    fund = models.takahashi_alexander(
        cc=inputs["cc"],
        rc=inputs["rc"],
        b=inputs["b"],
        g=inputs["g"],
        y=inputs["y"],
        nav=inputs["nav"],
        age=inputs["age"],
        pic=inputs["pic"],
    )
    output = analytics.metrics(
        fund,
        cc=inputs["cc"],
        nav=inputs["nav"],
        pic=inputs["pic"],
        distributions=inputs["distributions"],
    )
    pdt.assert_series_equal(output.round(2), expected_df, check_exact=False, atol=0.01)
