import marimo

__generated_with = "0.20.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib import ticker as tck

    sns.set(context="notebook", style="ticks")
    return mo, plt, sns, tck


@app.cell
def _():
    from privates.models import takahashi_alexander

    return (takahashi_alexander,)


@app.cell
def _(takahashi_alexander):
    fund = takahashi_alexander(
        **{
            "cc": 1_000_000.00,
            "rc": [0.25, 1 / 3, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.0],
            "b": 2.3,
            "g": 0.15,
            "y": 0.0,
            "nav": 0.0,
            "age": 0,
            "pic": 0.0,
        },
    )
    return (fund,)


@app.cell
def _(fund, mo):
    mo.ui.dataframe(
        fund,
        format_mapping={
            "NAV": "{:,.2f}".format,
            "Capital Call": "{:,.2f}".format,
            "Distribution": "{:,.2f}".format,
        },
    )
    return


@app.cell
def _(fund, mo, plt, sns, tck):
    fig, ax = plt.subplots()

    _tmp = fund.copy()
    _tmp["Net Cash Flow (cum.)"] = (
        _tmp["Distribution"] - _tmp["Capital Call"]
    ).cumsum()
    _tmp = _tmp / _tmp["Capital Call"].sum()
    ax = _tmp.plot(ax=ax)

    ax.set_xlim(fund.index.min(), fund.index.max())
    # ax.set_ylim(0)

    ax.xaxis.set_major_locator(tck.MultipleLocator(1))
    ax.yaxis.set_major_locator(tck.MultipleLocator(0.1))
    ax.set_ylabel("Multiple of Committed Capital")

    sns.despine(ax=ax)
    fig.tight_layout()
    del _tmp
    mo_ax = mo.ui.matplotlib(ax)
    mo_ax
    return


if __name__ == "__main__":
    app.run()
