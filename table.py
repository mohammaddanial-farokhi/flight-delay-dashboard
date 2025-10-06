from bokeh.models import ColumnDataSource, TableColumn, DataTable, TabPanel
from bokeh.layouts import column
import pandas as pd
import numpy as np


def table_tab(data):
    d = data.groupby("name")["arr_delay"].describe().reset_index()
    d = d.round(2)
    source = ColumnDataSource(d)

    tableC = [
        TableColumn(field="name", title="نام شرکت", width=550),
        TableColumn(field="count", title="تعداد پرواز"),
        TableColumn(field="mean", title="میانگین"),
        TableColumn(field="std", title="انحراف معیار"),
        TableColumn(field="min", title="کمترین تأخیر"),
        TableColumn(field="25%", title="چارک اول"),
        TableColumn(field="50%", title="چارک دوم"),
        TableColumn(field="75%", title="چارک سوم"),
        TableColumn(field="max", title="بیشترین تأخیر"),
    ]

    flight_table = DataTable(source=source, columns=tableC, width=1000, height=500)

    layout = column(flight_table)
    tab = TabPanel(child=layout, title="پنل جدول")

    return tab
