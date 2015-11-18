from collections import OrderedDict
from bokeh.plotting import figure
from bokeh.models import HoverTool

from bokeh._legacy_charts import Bar
from us_map_dataplot import us_map_data_source


TOOLS = "pan,reset,hover,save"


def plot_stacked_bar_chart(df, label_x, label_y, my_colors, is_stacked=False, lg_pos='top_right'):
    """ :return:Returns the bar chart object for the input dataframe  """

    bar = Bar(df, df.index.tolist(), stacked=is_stacked, responsive=True, legend=lg_pos,
              height=550, width=950, tools=TOOLS, xlabel=label_x, ylabel=label_y, palette=my_colors)
    return bar


def make_us_map(df_state_map):
    """ Plot of US Long-haul fiber optics connection statistics
    Signature : hover_text, plot_fig = make_us_map()
    """
    sources = us_map_data_source(df_state_map)

    plot = figure(tools=TOOLS, plot_width=950, plot_height=500, responsive=True)
    plot.patches('x', 'y', fill_color='color', line_color="#333333", line_width=0.5, source=sources)

    # Configure the tooltips
    hover = plot.select(dict(type=HoverTool))
    hover.point_policy = "follow_mouse"
    hover.tooltips = OrderedDict([
        ("Name ", "@name"),
        ("Incoming Fiber Links ", " @incoming"),
        ("Outgoing Fiber Links ", " @outgoing")
    ])
    return hover, plot
