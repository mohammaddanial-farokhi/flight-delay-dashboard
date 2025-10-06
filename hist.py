from bokeh.palettes import Category20_16
from bokeh.models import CheckboxGroup, ColumnDataSource, Slider, RangeSlider, TabPanel
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import column, row


def hist_tab(data):

    def md(s_data, rs=-60, re=120, bin=10):
        cols = ["proportion", "left", "right", "f_proportion", "f_interval", "name", "color"]
        if not s_data:
            empty = {c: [] for c in cols}
            return ColumnDataSource(empty)

        d = pd.DataFrame(columns=cols)
        r = re - rs
        n_bins = max(1, int(r / bin))
        for i, r_data in enumerate(s_data):
            subset = data[data["name"] == r_data]
            arr_hist, edge = np.histogram(subset["arr_delay"], bins=n_bins, range=(rs, re))
            total = np.sum(arr_hist)
            proportions = arr_hist / total if total > 0 else np.zeros_like(arr_hist, dtype=float)
            arr_df = pd.DataFrame({"proportion": proportions, "left": edge[:-1], "right": edge[1:]})
            arr_df["f_proportion"] = ["{:.5f}".format(p) for p in arr_df["proportion"]]
            arr_df["f_interval"] = [
                f"{left} to {right} minutes" for left, right in zip(arr_df["left"], arr_df["right"])
            ]
            arr_df["name"] = r_data
            arr_df["color"] = Category20_16[i % len(Category20_16)]
            d = pd.concat([d, arr_df], ignore_index=True)

        d = d.sort_values(["name", "left"])
        return ColumnDataSource(d)

    air_lines = sorted(data["name"].unique())
    chbox = CheckboxGroup(labels=air_lines, active=[0, 1, 2])
    slider = Slider(start=1, end=30, step=1, value=5, title="دسته بندی هیستوگرام")
    range_slider = RangeSlider(start=-60, end=180, step=5, value=(-60, 120), title="بازه تاخیر ها")

    init_data = [chbox.labels[i] for i in chbox.active]
    src = md(init_data, rs=range_slider.value[0], re=range_slider.value[1], bin=slider.value)

    p = figure(width=700, height=700, title="تاخیر در پرواز")
    p.quad(
        source=src,
        bottom=0,
        top="proportion",
        left="left",
        right="right",
        color="color",
        fill_alpha=0.7,
        legend_field="name",
    )

    def update(attr, old, new):
        air_line_checked = [chbox.labels[i] for i in chbox.active]
        new_src = md(air_line_checked, rs=range_slider.value[0], re=range_slider.value[1], bin=slider.value)
        src.data = dict(new_src.data)

    chbox.on_change("active", update)
    slider.on_change("value", update)
    range_slider.on_change("value", update)

    w = column(chbox, slider, range_slider)
    l = row(w, p)

    tab = TabPanel(child=l, title="پنل هیستوگرام")

    return l, tab
