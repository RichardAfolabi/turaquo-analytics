from collections import OrderedDict
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.sampledata import us_states
from fiber_functions import find_states_missing
from fiber_optics_dataset import state_map


# The plotting
TOOLS = "pan,reset,hover,save"

colors = ["#D1E2F2", "#ADCCE5", "#77B0D4", "#448BC0", "#2B62B2", "#2264AB", "#0D408E", "#294F70", "#273A48"]


def assign_color(codex):
    """ Assign specific color contrast to state based on link difference. """
    link_diff = state_map.State_Difference.ix[codex]
    if link_diff < 0:               # Outgoing more than incoming links
        colr = "#ED8466"            # Negative => Light Red
    else:                           # incoming link > outgoing, Link diff > 0.
        colr = colors[min(link_diff, len(colors))]   # Assign one of the color contrasts
    return colr


def us_map_data_source(df_state_map):
    """ Returns a ColumnDatasource containing the plotting elements """

    missing_states = find_states_missing(state_map)

    state_names = []
    state_colors = []
    state_incoming_link = []
    state_outgoing_link = []

    usa_states = us_states.data.copy()
    del usa_states['AK']
    del usa_states['HI']

    # fxn_state_map = df_state_map.sort_values('State_Difference', ascending=False)

    us_state_xs = [usa_states[code]["lons"] for code in usa_states]
    us_state_ys = [usa_states[code]["lats"] for code in usa_states]

    # Iterate over US Long/Lat list.
    for code in usa_states:
        # If code exist for infrastructure state
        if code in state_map.index.values:
            state_colors.append(assign_color(code))
            state_names.append(df_state_map.US_States.ix[code])
            state_incoming_link.append(df_state_map.Incoming_State.ix[code])
            state_outgoing_link.append(df_state_map.Outgoing_State.ix[code])
        else:
            # No link in State. state is missing.
            state_colors.append('#979383')        # Shade of gray
            state_names.append(missing_states.US_States.ix[code])
            state_incoming_link.append(0)
            state_outgoing_link.append(0)

    sources = ColumnDataSource(
        data=dict(
            x=us_state_xs,
            y=us_state_ys,
            color=state_colors,
            name=state_names,
            incoming=state_incoming_link,
            outgoing=state_outgoing_link
        ))
    return sources


def make_us_map(df_state_map):
    """ Plot of US Long-haul fiber optics connection statistics
    Signature : hover_text, plot_fig = make_us_map()
    """
    sources = us_map_data_source(df_state_map)

    plot = figure(tools=TOOLS, plot_width=850, plot_height=500, toolbar_location='left', responsive=True)
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
