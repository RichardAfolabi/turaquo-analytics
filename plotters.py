
from bokeh._legacy_charts import Bar

TOOLS = "pan,reset,hover,save"


def plot_stacked_bar_chart(df, label_x, label_y, my_colors, is_stacked=False, lg_pos='top_right'):
    """
    :return:Returns the bar chart object for the input dataframe.
    """
    bar = Bar(df, df.index.tolist(), stacked=is_stacked, responsive=True, legend=lg_pos,
              height=500, width=950, tools=TOOLS, xlabel=label_x, ylabel=label_y, palette=my_colors)
    return bar
