import pandas as pd
import json

def percentageNEDGreenEnergySingleDay(object_SolarInput_SingleDay, object_WindInput_SingleDay, object_TotalMixInput_SingleDay, dateValueStrFormat):

    '''
    Param (Str): dateValueStrFormat : Sample: '2025-03-22'
    Param (JSON): object_SolarInput_SingleDay | object_WindInput_SingleDay | object_TotalMixInput_SingleDay : List of objects. Sample:
        [
    {
        "@id": "/v1/utilizations/68639887481",
        "@type": "Utilization",
        "id": 68639887481,
        "point": "/v1/points/0",
        "type": "/v1/types/1",
        "granularity": "/v1/granularities/4",
        "granularitytimezone": "/v1/granularity_time_zones/0",
        "activity": "/v1/activities/1",
        "classification": "/v1/classifications/2",
        "capacity": 431688,
        "volume": 107922,
        "percentage": 0.06511380523443222,
        "emission": 0,
        "emissionfactor": 0,
        "validfrom": "2025-03-20T23:00:00+00:00",
        "validto": "2025-03-20T23:15:00+00:00",
        "lastupdate": "2025-03-22T23:52:25+00:00"
    },
    {
        "@id": "/v1/utilizations/68639949251",
        "@type": "Utilization",
        "id": 68639949251,
        "point": "/v1/points/0",
        "type": "/v1/types/1",
        "granularity": "/v1/granularities/4",
        "granularitytimezone": "/v1/granularity_time_zones/0",
        "activity": "/v1/activities/1",
        "classification": "/v1/classifications/2",
        "capacity": 458324,
        "volume": 114581,
        "percentage": 0.06913135200738907,
        "emission": 0,
        "emissionfactor": 0,
        "validfrom": "2025-03-20T23:15:00+00:00",
        "validto": "2025-03-20T23:30:00+00:00",
        "lastupdate": "2025-03-22T23:52:25+00:00"
    },
    .
    .
    .]
    '''
    object_SolarInput_SingleDay_json = json.loads(object_SolarInput_SingleDay)
    object_WindInput_SingleDay_json = json.loads(object_WindInput_SingleDay)
    object_TotalMixInput_SingleDay_json = json.loads(object_TotalMixInput_SingleDay)

    df_single_Solar = pd.DataFrame(object_SolarInput_SingleDay_json)
    df_single_Wind = pd.DataFrame(object_WindInput_SingleDay_json)
    df_single_totalmix = pd.DataFrame(object_TotalMixInput_SingleDay_json)

    df_single_Solar['validfrom'] = pd.to_datetime(df_single_Solar['validfrom'])
    df_single_Wind['validfrom'] = pd.to_datetime(df_single_Wind['validfrom'])
    df_single_totalmix['validfrom'] = pd.to_datetime(df_single_totalmix['validfrom'])

    df_single_Solar['validfrom_date'] = pd.to_datetime(df_single_Solar['validfrom']).dt.date
    df_single_Wind['validfrom_date'] = pd.to_datetime(df_single_Wind['validfrom']).dt.date
    df_single_totalmix['validfrom_date'] = pd.to_datetime(df_single_totalmix['validfrom']).dt.date

    df_single_Solar['validfrom_date'] = df_single_Solar['validfrom_date'].astype(str)
    df_single_Wind['validfrom_date'] = df_single_Wind['validfrom_date'].astype(str)
    df_single_totalmix['validfrom_date'] = df_single_totalmix['validfrom_date'].astype(str)

    df_single_Solar = df_single_Solar[df_single_Solar['validfrom_date']==dateValueStrFormat]
    df_single_Wind = df_single_Wind[df_single_Wind['validfrom_date']==dateValueStrFormat]
    df_single_totalmix = df_single_totalmix[df_single_totalmix['validfrom_date']==dateValueStrFormat]

    df_single_Solar_filtered = df_single_Solar[['validfrom','volume']]
    df_single_Solar_filtered = df_single_Solar_filtered.sort_values(by='validfrom')
    df_single_Solar_filtered.rename(columns={'volume': 'volume_Solar'}, inplace=True)
    df_single_Solar_filtered['validfrom'] = df_single_Solar_filtered['validfrom'].astype(str)

    df_single_Wind_filtered = df_single_Wind[['validfrom','volume']]
    df_single_Wind_filtered = df_single_Wind_filtered.sort_values(by='validfrom')
    df_single_Wind_filtered.rename(columns={'volume': 'volume_Wind'}, inplace=True)
    df_single_Wind_filtered['validfrom'] = df_single_Wind_filtered['validfrom'].astype(str)

    df_single_totalmix_filtered = df_single_totalmix[['validfrom','volume']]
    df_single_totalmix_filtered = df_single_totalmix_filtered.sort_values(by='validfrom')
    df_single_totalmix_filtered.rename(columns={'volume': 'volume_TotalMix'}, inplace=True)
    df_single_totalmix_filtered['validfrom'] = df_single_totalmix_filtered['validfrom'].astype(str)

    df_Complete = df_single_Solar_filtered.merge(df_single_Wind_filtered, on='validfrom', how='left')
    df_Complete = df_Complete.merge(df_single_totalmix_filtered, on='validfrom', how='left')

    df_Complete['Solar_Percentage'] = (df_Complete['volume_Solar']/df_Complete['volume_TotalMix'])*100
    df_Complete['Wind_Percentage'] = (df_Complete['volume_Wind']/df_Complete['volume_TotalMix'])*100

    df_Complete['TotalGreen_Percentage'] = (df_Complete['Solar_Percentage'] + df_Complete['Wind_Percentage'])

    return df_Complete.to_json(orient='records')


def greenBehaviourPercentagesSingleDaySingleNonSolarUser(object_meterreading_bencompare, object_SolarInput_SingleDay, object_WindInput_SingleDay, object_TotalMixInput_SingleDay, dateValueStrFormat):

    object_meterreading_bencompare_json = json.loads(object_meterreading_bencompare)
    object_SolarInput_SingleDay_json = json.loads(object_SolarInput_SingleDay)
    object_WindInput_SingleDay_json = json.loads(object_WindInput_SingleDay)
    object_TotalMixInput_SingleDay_json = json.loads(object_TotalMixInput_SingleDay)

    df_meterreading_bencompare = pd.DataFrame(object_meterreading_bencompare_json)
    df_single_Solar = pd.DataFrame(object_SolarInput_SingleDay_json)
    df_single_Wind = pd.DataFrame(object_WindInput_SingleDay_json)
    df_single_totalmix = pd.DataFrame(object_TotalMixInput_SingleDay_json)

    df_meterreading_bencompare['Items_Timestamp_UTC'] = pd.to_datetime(df_meterreading_bencompare['Items_Timestamp_UTC'])
    df_single_Solar['validfrom'] = pd.to_datetime(df_single_Solar['validfrom'])
    df_single_Wind['validfrom'] = pd.to_datetime(df_single_Wind['validfrom'])
    df_single_totalmix['validfrom'] = pd.to_datetime(df_single_totalmix['validfrom'])

    df_meterreading_bencompare['Items_Timestamp_UTC_date'] = pd.to_datetime(df_meterreading_bencompare['Items_Timestamp_UTC']).dt.date
    df_single_Solar['validfrom_date'] = pd.to_datetime(df_single_Solar['validfrom']).dt.date
    df_single_Wind['validfrom_date'] = pd.to_datetime(df_single_Wind['validfrom']).dt.date
    df_single_totalmix['validfrom_date'] = pd.to_datetime(df_single_totalmix['validfrom']).dt.date


    df_meterreading_bencompare['Items_Timestamp_UTC_date'] = df_meterreading_bencompare['Items_Timestamp_UTC_date'].astype(str)
    df_single_Solar['validfrom_date'] = df_single_Solar['validfrom_date'].astype(str)
    df_single_Wind['validfrom_date'] = df_single_Wind['validfrom_date'].astype(str)
    df_single_totalmix['validfrom_date'] = df_single_totalmix['validfrom_date'].astype(str)

    df_meterreading_bencompare = df_meterreading_bencompare[df_meterreading_bencompare['Items_Timestamp_UTC_date']==dateValueStrFormat]
    df_single_Solar = df_single_Solar[df_single_Solar['validfrom_date']==dateValueStrFormat]
    df_single_Wind = df_single_Wind[df_single_Wind['validfrom_date']==dateValueStrFormat]
    df_single_totalmix = df_single_totalmix[df_single_totalmix['validfrom_date']==dateValueStrFormat]

    df_meterreading_bencompare_filtered = df_meterreading_bencompare[['Items_Timestamp_UTC','Items_ConsumptionDeliveryTotal']]
    df_meterreading_bencompare_filtered = df_meterreading_bencompare_filtered.sort_values(by='Items_Timestamp_UTC')
    df_meterreading_bencompare_filtered.rename(columns={'Items_ConsumptionDeliveryTotal': 'ConsumptionDeliveryTotal'}, inplace=True)
    df_meterreading_bencompare_filtered['Items_Timestamp_UTC'] = df_meterreading_bencompare_filtered['Items_Timestamp_UTC'].astype(str)
    
    df_single_Solar_filtered = df_single_Solar[['validfrom','volume']]
    df_single_Solar_filtered = df_single_Solar_filtered.sort_values(by='validfrom')
    df_single_Solar_filtered.rename(columns={'volume': 'volume_Solar'}, inplace=True)
    df_single_Solar_filtered['validfrom'] = df_single_Solar_filtered['validfrom'].astype(str)

    df_single_Wind_filtered = df_single_Wind[['validfrom','volume']]
    df_single_Wind_filtered = df_single_Wind_filtered.sort_values(by='validfrom')
    df_single_Wind_filtered.rename(columns={'volume': 'volume_Wind'}, inplace=True)
    df_single_Wind_filtered['validfrom'] = df_single_Wind_filtered['validfrom'].astype(str)

    df_single_totalmix_filtered = df_single_totalmix[['validfrom','volume']]
    df_single_totalmix_filtered = df_single_totalmix_filtered.sort_values(by='validfrom')
    df_single_totalmix_filtered.rename(columns={'volume': 'volume_TotalMix'}, inplace=True)
    df_single_totalmix_filtered['validfrom'] = df_single_totalmix_filtered['validfrom'].astype(str)

    df_Complete = df_single_Solar_filtered.merge(df_single_Wind_filtered, on='validfrom', how='left')
    df_Complete = df_Complete.merge(df_single_totalmix_filtered, on='validfrom', how='left')
    df_Complete = df_Complete.merge(df_meterreading_bencompare_filtered,  left_on='validfrom', right_on='Items_Timestamp_UTC', how='left')

    df_Complete['Solar_Percentage'] = (df_Complete['volume_Solar']/df_Complete['volume_TotalMix'])*100
    df_Complete['Wind_Percentage'] = (df_Complete['volume_Wind']/df_Complete['volume_TotalMix'])*100

    df_Complete['TotalGreen_Percentage'] = (df_Complete['Solar_Percentage'] + df_Complete['Wind_Percentage'])

    df_Complete['TotalNoGreen_Percentage'] = (100 - df_Complete['TotalGreen_Percentage'])

    df_Complete['ConsumptionDeliveryTotal_Green'] = (df_Complete['ConsumptionDeliveryTotal']*df_Complete['TotalGreen_Percentage'])/100
    df_Complete['ConsumptionDeliveryTotal_NoGreen'] = (df_Complete['ConsumptionDeliveryTotal']*df_Complete['TotalNoGreen_Percentage'])/100

    df_Complete_total_consumption_singleDay = df_Complete['ConsumptionDeliveryTotal'].sum()
    df_Complete_total_Green_consumption_singleDay = df_Complete['ConsumptionDeliveryTotal_Green'].sum()

    green_percentage_consumtpion_single_day = (df_Complete_total_Green_consumption_singleDay/df_Complete_total_consumption_singleDay)*100
    df_Complete_total_Green_production_singleDay = df_Complete['TotalGreen_Percentage'].mean()

    return green_percentage_consumtpion_single_day, df_Complete_total_Green_production_singleDay


# def greenBehaviourPercentagesSingleDaySingleNonSolarUser(object_meterreading_bencompare, object_SolarInput_SingleDay, object_WindInput_SingleDay, object_TotalMixInput_SingleDay, dateValueStrFormat):

#     df_single_Solar = pd.DataFrame(object_SolarInput_SingleDay)
#     df_single_Wind = pd.DataFrame(object_WindInput_SingleDay)
#     df_single_totalmix = pd.DataFrame(object_TotalMixInput_SingleDay)

#     df_single_Solar['validfrom'] = pd.to_datetime(df_single_Solar['validfrom'])
#     df_single_Solar_filtered = df_single_Solar[['validfrom','volume']]
#     df_single_Solar_filtered = df_single_Solar_filtered.sort_values(by='validfrom')
#     df_single_Solar_filtered.rename(columns={'volume': 'volume_Solar'}, inplace=True)
#     df_single_Solar_filtered['validfrom'] = df_single_Solar_filtered['validfrom'].astype(str)
    
#     df_single_Wind['validfrom'] = pd.to_datetime(df_single_Wind['validfrom'])
#     df_single_Wind_filtered = df_single_Wind[['validfrom','volume']]
#     df_single_Wind_filtered = df_single_Wind_filtered.sort_values(by='validfrom')
#     df_single_Wind_filtered.rename(columns={'volume': 'volume_Wind'}, inplace=True)
#     df_single_Wind_filtered['validfrom'] = df_single_Wind_filtered['validfrom'].astype(str)

#     df_single_totalmix['validfrom'] = pd.to_datetime(df_single_totalmix['validfrom'])
#     df_single_totalmix_filtered = df_single_totalmix[['validfrom','volume']]
#     df_single_totalmix_filtered = df_single_totalmix_filtered.sort_values(by='validfrom')
#     df_single_totalmix_filtered.rename(columns={'volume': 'volume_TotalMix'}, inplace=True)
#     df_single_totalmix_filtered['validfrom'] = df_single_totalmix_filtered['validfrom'].astype(str)

#     df_Complete = df_single_Solar_filtered.merge(df_single_Wind_filtered, on='validfrom', how='left')
#     df_Complete = df_Complete.merge(df_single_totalmix_filtered, on='validfrom', how='left')

#     df_Complete['Solar_Percentage'] = (df_Complete['volume_Solar']/df_Complete['volume_TotalMix'])*100
#     df_Complete['Wind_Percentage'] = (df_Complete['volume_Wind']/df_Complete['volume_TotalMix'])*100

#     df_Complete['TotalGreen_Percentage'] = (df_Complete['Solar_Percentage'] + df_Complete['Wind_Percentage'])

#     df_Complete['Green_percentage_normalized_0_to_1'] = (df_Complete['TotalGreen_percentage'] - df_Complete['TotalGreen_percentage'].min()) / (df_Complete['TotalGreen_percentage'].max() - df_Complete['TotalGreen_percentage'].min())

#     # Bencompare Usage
#     df_MeterReading_NonSolar = pd.read_csv("MeterReading_NoSolar_sample_CSV_Treated_t.csv", header=0)
#     df_MeterReading_NonSolar = df_MeterReading_NonSolar[df_MeterReading_NonSolar['Items_Timestamp_UTC_date']==SingleDateValue]

#     percentage_consumption_NonSolarUser = df_MeterReading_NonSolar.merge(df_Complete, left_on='Items_Timestamp_UTC', right_on='validfrom', how='left')
#     percentage_consumption_NonSolarUser['green_precentage_household'] = percentage_consumption_NonSolarUser['Items_ConsumptionDeliveryTotal']*percentage_consumption_NonSolarUser['Green_percentage_normalized_0_to_1']

#     percentage_consumption_NonSolarUser['Nogreen_precentage_household'] = 1 - percentage_consumption_NonSolarUser['green_precentage_household']

