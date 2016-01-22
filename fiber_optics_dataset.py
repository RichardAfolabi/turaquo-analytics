
import pandas as pd
from fiber_functions import postalcode_scraper

postalcode_table = postalcode_scraper()

# Load Node dataset from Amazon S3
column_names = ['Nodes_City_State']
node_url = "https://s3-us-west-2.amazonaws.com/telecoms-analytics-dataset/nodes.txt"
node_city_state = pd.read_csv(node_url, sep='\t', header=None, index_col=0, names=column_names)

# Load edges dataset from Amazon S3
column_names = ['Source', 'Sink']
edges_url = "https://s3-us-west-2.amazonaws.com/telecoms-analytics-dataset/links.txt"
edges_src_snk = pd.read_csv(edges_url, names=column_names, header=None)

# Merge both Source and Sink dataframes  with the corresponding codes
on_Source = pd.merge(edges_src_snk, node_city_state, left_on=['Source'], right_index=True)
source_sink = pd.merge(on_Source, node_city_state, left_on=['Sink'], right_index=True)

# Rename the resulting columns and sort the index 'inplace'
column_names = ['Source_Index', 'Sink_Index', 'Incoming', 'Outgoing']
source_sink.columns = column_names
source_sink.sort_index(inplace=True)

# Get the frequency of Incoming and Outgoing sites and merge into a single Dataframe
all_incoming_outgoing = pd.merge(pd.DataFrame(source_sink['Incoming'].value_counts()),
                                 pd.DataFrame(source_sink['Outgoing'].value_counts()),
                                 left_index=True, right_index=True)

# What Locations have the HIGHEST INCOMING fiber Links?
highest_incoming_loc = all_incoming_outgoing.sort_values('Incoming', ascending=False)

# the Locations with HIGHEST OUTGOING fiber connections
lowest_outgoing_loc = all_incoming_outgoing.sort_values(['Outgoing'])
lowest_outgoing_loc = lowest_outgoing_loc.reindex(columns=['Outgoing', 'Incoming'])


# Add new Cities and States columns to the Dataframe
source_sink['Incoming_City'] = ''
source_sink['Outgoing_City'] = ''
source_sink['Incoming_State'] = ''
source_sink['Outgoing_State'] = ''

for ndx in source_sink.index:
    # Split both incoming and outgoing on colon to City and State
    incoming = source_sink.Incoming[ndx].split(';')
    outgoing = source_sink.Outgoing[ndx].split(';')

    # Populate the Incoming Cities
    source_sink['Incoming_City'].values[ndx] = incoming[0]
    source_sink['Outgoing_City'].values[ndx] = outgoing[0]

    # If the State is mising, use the City e.g. Washington DC
    source_sink['Incoming_State'].values[ndx] = incoming[1] if len(incoming) > 1 else incoming[0]
    source_sink['Outgoing_State'].values[ndx] = outgoing[1] if len(outgoing) > 1 else outgoing[0]

# Form new dataframe
new_source_sink = source_sink.drop(['Source_Index', 'Sink_Index', 'Incoming', 'Outgoing'], axis=1)


# CITIES - Top 5 and Lowest 5 Cities with Average Link Connection Difference
city_in_out_diff = pd.merge(pd.DataFrame(new_source_sink['Incoming_City'].value_counts()),
                            pd.DataFrame(new_source_sink['Outgoing_City'].value_counts()),
                            left_index=True, right_index=True)

city_in_out_diff['City_Difference'] = ((city_in_out_diff.Incoming_City -
                                        city_in_out_diff.Outgoing_City) / city_in_out_diff.Incoming_City) * 100

city_in_out_diff = city_in_out_diff.sort_values('City_Difference', ascending=False)

top5_low5 = [city_in_out_diff.head(), city_in_out_diff.tail()]
top5_low5 = pd.concat(top5_low5)


# STATES - Top 5 and Lowest 5 STATES with Average Link Connection Difference
state_in_out_diff = pd.merge(pd.DataFrame(new_source_sink['Incoming_State'].value_counts()),
                             pd.DataFrame(new_source_sink['Outgoing_State'].value_counts()),
                             left_index=True, right_index=True)

state_in_out_diff['State_Difference'] = ((state_in_out_diff.Incoming_State -
                                          state_in_out_diff.Outgoing_State) / state_in_out_diff.Incoming_State) * 100

state_in_out_diff = state_in_out_diff.sort_values('State_Difference', ascending=False)

smp = state_in_out_diff.State_Difference

in_out_state = pd.DataFrame(pd.concat([smp.head(4), smp.ix[-2:-15:-2]]))
in_out_state.sort_values('State_Difference', ascending=False, inplace=True)
state_diff = in_out_state.transpose()


# Top 10 states with HIGHEST INCOMING & LOWEST OUTGOING links
the_states = state_in_out_diff[['Incoming_State', 'Outgoing_State']].copy()
top_states_inc = the_states.sort_values('Incoming_State', ascending=False).head(10)
low_states_outg = the_states.sort_values('Outgoing_State', ascending=False).tail(10)
low_states_outg = low_states_outg.reindex(columns=['Outgoing_State', 'Incoming_State'])


# ANALYSIS
# ===========

# CITIES - Incoming vs Outgoing vs City_Difference, etc
city_in_out_diff['City_Difference'] = city_in_out_diff.Incoming_City - city_in_out_diff.Outgoing_City


# Incoming State vs Outgoing State
state_in_out_diff['State_Difference'] = state_in_out_diff.Incoming_State - state_in_out_diff.Outgoing_State
state_in_out_diff = state_in_out_diff.sort_values('State_Difference', ascending=False)


# MAP VISUALIZATION
# Merge result of scraping with existing dataframe
state_map = state_in_out_diff[['Incoming_State', 'Outgoing_State']].copy()
state_map['State_Difference'] = state_map.Incoming_State - state_map.Outgoing_State

state_map = pd.merge(state_map, postalcode_table, left_index=True, right_index=True, how='left')


# Since Washington DC has no state, we can directly encode as 'DC
state_map.ix['Washington_DC'] = state_map.ix['Washington_DC'].fillna('DC')


state_map['US_States'] = state_map.index
state_map.index = state_map.PostalCode
state_map.drop('PostalCode', axis=1, inplace=True)
