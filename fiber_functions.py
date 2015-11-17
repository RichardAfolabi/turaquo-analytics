
import pandas as pd
# Scrape web data for US States Abbreviations and Postal Codes.   http://www.infoplease.com/ipa/A0110468.html


def postalcode_scraper():
    """
    Scrapes a known URL and returns a Pandas dataframe containing
    list of US States as index and their Postal Codes as column values.
    """

    data_url = "http://www.infoplease.com/ipa/A0110468.html"
    
    # Scrape the page with Pandas 
    table_scrape = pd.read_html(data_url)[1]
    
    # Subtitute spaces in State names with '_' to confirm with existing dataset
    table_scrape[0] = [tab.replace(' ', '_') for tab in table_scrape[0]]
    
    # Reindex using corrected state names to confirm to existing dataframe formats
    table_scrape.index = table_scrape[0]
    
    # Remove extranous data elements and unneeded columns
    table_scrape.drop([0, 1], axis=1, inplace=True)
    table_scrape.drop('State', inplace=True)

    # Set column and index names.
    table_scrape.index.name = 'State'
    table_scrape.columns = ['PostalCode']

    return table_scrape


def find_states_missing(df):
    """ Returns dataframe of states missing from our dataset """

    states_missing = []
    postcodes = postalcode_scraper()

    for st in postcodes.PostalCode:
        if st not in df.index:
            d = postcodes.loc[postcodes['PostalCode'] == st]
            states_missing.append(d)

    states_missing = pd.concat(states_missing)
    states_missing['US_States'] = states_missing.index
    states_missing.index = states_missing.PostalCode.values
    states_missing.drop('PostalCode', axis=1, inplace=True)

    return states_missing
