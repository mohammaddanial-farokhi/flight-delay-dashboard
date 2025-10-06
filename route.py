from bokeh.palettes import Category20_16
from bokeh.models import ColumnDataSource, Select, TabPanel
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import column, row
from itertools import chain


def route_tab(data):
    def make_dataset(user_origin, user_destanantion):
        user_choise = data[(data["origin"] == user_origin) & (data["dest"] == user_destanantion)]
        if user_choise.empty:
            return ColumnDataSource(data=dict(x=[], y=[], color=[], airline=[])), {}

        airlines_by_user = sorted(user_choise["name"].unique())
        colors = Category20_16 * ((len(airlines_by_user) // 16) + 1)

        x, y, color, airline = [], [], [], []

        for i, j in enumerate(airlines_by_user):
            airline_flights = user_choise[user_choise["name"] == j]
            x.extend(airline_flights["arr_delay"])
            y.extend([j] * len(airline_flights))  # اسم شرکت، نه عدد
            color.extend([colors[i]] * len(airline_flights))
            airline.extend([j] * len(airline_flights))

        return ColumnDataSource(data=dict(x=x, y=y, color=color, airline=airline)), {}

    from bokeh.models import FactorRange

    def make_plot(src, origin_init, destanations_init, airline_dict):
        y_categories = sorted(list(set(src.data["y"]))) or ["—"]

        p = figure(
            title=f"مسیر {origin_init} → {destanations_init}",
            x_axis_label="تاخیر ورود (دقیقه)",
            y_axis_label="شرکت هواپیمایی",
            height=400,
            width=700,
            y_range=FactorRange(*y_categories),  # 👈 تغییر مهم
        )

        p.scatter("x", "y", source=src, color="color", size=8, alpha=0.6)
        return p

    all_origins = list(set(data["origin"]))
    all_destanations = list(set(data["dest"]))

    origins_select = Select(title="انتخاب مبدا", value="EWR", options=all_origins)
    destanations_select = Select(title="انتخاب مقصد", value="IAH", options=all_destanations)

    origin_init = origins_select.value
    destanations_init = destanations_select.value

    src, airline_dict = make_dataset(origin_init, destanations_init)
    p = make_plot(src, origin_init, destanations_init, airline_dict)

    def update(attr, old, new):
        selected_origin = origins_select.value
        selected_destanation = destanations_select.value
        new_src, new_dict = make_dataset(selected_origin, selected_destanation)
        src.data = dict(new_src.data)
        p.y_range.factors = sorted(list(set(new_src.data["y"]))) or ["—"]
        p.title.text = f"مسیر {selected_origin} → {selected_destanation}"

    origins_select.on_change("value", update)
    destanations_select.on_change("value", update)

    selectors_place = column(origins_select, destanations_select)
    final_layoout = row(selectors_place, p)
    final_tab = TabPanel(child=final_layoout, title="مبدا / مقصد")
    return final_tab
