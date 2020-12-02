import pandas as pd
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.graph_objs import *

#import data
covid_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
iso_code_url = "https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv"

#create dataframes
covid_df = pd.read_csv(covid_url)
population_df = pd.read_csv("population_by_country_2020.csv")
iso_df = pd.read_csv(iso_code_url)

#extract specific areas
extract_list = ["Greenland"]

#standardize and combine dataframes
iso_df = pd.concat([iso_df.iloc[:,2], iso_df.iloc[:,41]], axis=1).reset_index(drop=True)
iso_df = iso_df.rename(columns={"ISO3166-1-Alpha-3":"ISO", "official_name_en":"Country"})
iso_df = iso_df.dropna()
iso_df = iso_df.replace({"United States of America":"United States"})
iso_df = iso_df.replace({"Russian Federation":"Russia"})
iso_df = iso_df.replace({"Bolivia (Plurinational State of)":"Bolivia"})
iso_df = iso_df.replace({"Venezuela (Bolivarian Republic of)":"Venezuela"})
iso_df = iso_df.replace({"United Kingdom of Great Britain and Northern Ireland":"United Kingdom"})
iso_df = iso_df.replace({"Iran (Islamic Republic of)":"Iran"})
iso_df = iso_df.replace({"Republic of Korea":"South Korea"})
iso_df = iso_df.replace({"Democratic People's Republic of Korea":"North Korea"})
iso_df = iso_df.replace({"United Republic of Tanzania":"Tanzania"})
iso_df = iso_df.replace({"Democratic Republic of the Congo":"DR Congo"})

covid_df = covid_df.rename(columns={"Province/State":"Province", "Country/Region":"Country"})
province_df = covid_df.copy()
extracted_df = pd.DataFrame(columns=["Country", "Total_Cases"])
province_df = pd.concat([province_df.iloc[:,0], province_df.iloc[:,-1]], axis=1).reset_index(drop=True)
current_date = province_df.columns[1]
province_df = province_df.rename(columns={current_date:"Total_Cases"})
for row, col in province_df.iterrows():
    if col["Province"] in extract_list:
        new_row = {'Country' : col["Province"], 'Total_Cases' : int(col["Total_Cases"])}
        extracted_df = extracted_df.append(new_row, ignore_index=True)
        covid_df = covid_df[covid_df.Province != col["Province"]]

covid_df = covid_df.replace({"Congo (Brazzaville)":"Congo"})
covid_df = covid_df.replace({"Congo (Kinshasa)":"DR Congo"})
covid_df = covid_df.replace({"Korea, South":"South Korea"})
covid_df = covid_df.replace({"Democratic People's Republic of Korea":"North Korea"})
covid_df = covid_df.groupby(["Country"]).sum().reset_index()
covid_df = covid_df.replace({'US':"United States"})
covid_df = pd.concat([covid_df.iloc[:,0], covid_df.iloc[:,-1]], axis=1).reset_index(drop=True)
current_date = covid_df.columns[1]
covid_df = covid_df.rename(columns={current_date:"Total_Cases"})
covid_df = pd.merge(covid_df, extracted_df, how="outer", on=["Country", "Total_Cases"])
covid_df = pd.merge(covid_df, iso_df, how="outer", on="Country")


population_df = population_df.rename(columns={"Country (or dependency)":"Country", "Population (2020)":"Population"})
population_df = population_df.iloc[:,0:2]

df = pd.merge(covid_df, population_df, how="outer", on="Country")
df = df.dropna()
df = df.reset_index(drop=True)

#do calculations for percent of country infected
df["Percent_Infected"] = df["Total_Cases"]/df["Population"]*100
df["Percent_Infected"] = df["Percent_Infected"].apply(lambda x: round(x, 5))

#Remove outlier
#df = df[df.Country != "Andorra"]

df.to_csv('covid_world_percent_infected_data.csv', index=False)