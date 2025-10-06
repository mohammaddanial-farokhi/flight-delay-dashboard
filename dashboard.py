from bokeh.io import curdoc
import pandas as pd
from bokeh.models import Tabs
from hist import hist_tab
from table import table_tab
from route import route_tab


data = pd.read_csv("flights.csv")
layout, tab_hist = hist_tab(data)
tab_table = table_tab(data)
tab_route = route_tab(data)

finall = Tabs(tabs=[tab_hist, tab_table, tab_route])
curdoc().add_root(finall)
