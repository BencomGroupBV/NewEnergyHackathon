import pandas as pd

def percentageNEDGreenEnergySingleDay(object_SolarInput_SingleDay, object_WindInput_SingleDay, object_TotalMixInput_SingleDay, dateValueStrFormat):

    df_single_Solar = pd.DataFrame(object_SolarInput_SingleDay)
    df_single_Wind = pd.DataFrame(object_WindInput_SingleDay)
    df_single_totalmix = pd.DataFrame(object_TotalMixInput_SingleDay)

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

# def greenBehaviourScoreSingleDaySingleNonSolarUser(object_SolarInput_SingleDay, object_WindInput_SingleDay, object_TotalMixInput_SingleDay, SingleDateValue):

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

