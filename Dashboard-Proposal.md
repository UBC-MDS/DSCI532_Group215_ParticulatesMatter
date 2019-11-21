# Dashboard Proposal

## Section 1:  Motivation and Purpose


## Section 2 Description of the data

Our app will visualize data sourced from the BC Ministry of Environment and Climate Change. The ministry publishes quality-assured hourly data on its [website](https://catalogue.data.gov.bc.ca/dataset/77eeadf4-0c19-48bf-a47a-fa9eef01f409) from air quality monitoring stations across BC. The following columns in the dataset are pertinent to our app:
- Date and time of each observation is found in the `DATA_PST` variable in Pacific Standard Time;
- The location of each reading is found in the `STATION_NAME` variable, which is paired with a unique `EMS_ID`;
- The name of the specific pollutant measured is stored in the `PARAMETER` field; 
- The name of the instrument used to record pollutant concentrations is stored in the `INSTRUMENT` variable; and
- The concentrations of PM2.5 and PM10 are recorded in the `RAW_VALUE` amd `ROUNDED_VALUE` fields. The units corresponding to these concentrations are micrograms per cubic metre (ug/m3) as shown in the `UNITS` variable.


## Section 3: Research questions and usage scenarios


- Do concentration levels of PM10 and PM25 follow a similar trend?
- Do concentration levels of PM10 and PM25 exhibit seasonality
- Is there a particular season of the year which is characterized by the highest pollution levels?
- What is the range of average PM10 and PM25 concentrations in a given year?
- What is the rate of change from season to season for the time period?
- What locations have the highest concentration of pollutants? 
- Which location has the highest rate of increase for pollutant concentration.



The main point of the dashboard is to inform clients on how pollution has changed over time as well as where the pollution is most intense. 

Dave, BC’s  Commissioner for Sustainable Development and the Environment, is hoping to better understand the air quality situation in areas of Greater Vancouver, to track whether air quality is under control. He is particularly interested in what locations are most in need for interventions to lower pollutant concentration in the air. Our app, “Pollutants Matter BC”, is focused on delivering Dave methods of visualization to help inform him. For example, he may be specifically interested in the air pollution of coastal areas. He may hypothesize that coastal areas have seen a rise in air pollution in the past decade. Using the apps features to selectively toggle data for locations of interest, Dave will easily be able to track how PM10 and PM2.5 have changed over the years. Furthermore, he will be able to pinpoint which coastal areas are in the worst shape so that urgent action can be taken to reverse any worrying trends. 
