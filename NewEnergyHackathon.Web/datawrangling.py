import pandas as pd

def percentageNEDGreenEnergySingleDay(object_SolarInput_SingleDay, object_WindInput_SingleDay, object_TotalMixInput_SingleDay):

    df_single_Solar = pd.DataFrame(object_SolarInput_SingleDay)
    df_single_Wind = pd.DataFrame(object_WindInput_SingleDay)
    df_single_totalmix = pd.DataFrame(object_TotalMixInput_SingleDay)

    df_single_Solar['validfrom'] = pd.to_datetime(df_single_Solar['validfrom'])
    df_single_Solar_filtered = df_single_Solar[['validfrom','volume']]
    df_single_Solar_filtered = df_single_Solar_filtered.sort_values(by='validfrom')
    df_single_Solar_filtered.rename(columns={'volume': 'volume_Solar'}, inplace=True)
    df_single_Solar_filtered['validfrom'] = df_single_Solar_filtered['validfrom'].astype(str)
    
    df_single_Wind['validfrom'] = pd.to_datetime(df_single_Wind['validfrom'])
    df_single_Wind_filtered = df_single_Wind[['validfrom','volume']]
    df_single_Wind_filtered = df_single_Wind_filtered.sort_values(by='validfrom')
    df_single_Wind_filtered.rename(columns={'volume': 'volume_Wind'}, inplace=True)
    df_single_Wind_filtered['validfrom'] = df_single_Wind_filtered['validfrom'].astype(str)

    df_single_totalmix['validfrom'] = pd.to_datetime(df_single_totalmix['validfrom'])
    df_single_totalmix_filtered = df_single_totalmix[['validfrom','volume']]
    df_single_totalmix_filtered = df_single_totalmix_filtered.sort_values(by='validfrom')
    df_single_totalmix_filtered.rename(columns={'volume': 'volume_TotalMix'}, inplace=True)
    df_single_totalmix_filtered['validfrom'] = df_single_totalmix_filtered['validfrom'].astype(str)

    df_Complete = df_single_Solar_filtered.merge(df_single_Wind_filtered, on='validfrom', how='left')
    df_Complete = df_Complete.merge(df_single_totalmix_filtered, on='validfrom', how='left')

    df_Complete['Solar_Percentage'] = (df_Complete['volume_Solar']/df_Complete['volume_TotalMix'])*100
    df_Complete['Wind_Percentage'] = (df_Complete['volume_Wind']/df_Complete['volume_TotalMix'])*100

    df_Complete['TotalGreen_Percentage'] = (df_Complete['Solar_Percentage'] + df_Complete['Wind_Percentage'])
    # return
    return df_Complete.to_json(orient='records')

# def greenBehaviourScoreSingleDaySingleNonSolarUser(df_BencompareConsumptionDeliveryMarchComplete, json_GreenPercentageGridSingleDay, singleDateValue):

#     df_MeterReading_NonSolar = pd.read_csv("MeterReading_NoSolar_sample_CSV_Treated_t.csv", header=0)
#     df_MeterReading_NonSolar = df_MeterReading_NonSolar[df_MeterReading_NonSolar['Items_Timestamp_UTC_date']==singleDateValue]
#     df_greenPercentages = pd.DataFrame(json_GreenPercentageGridSingleDay)

#     percentage_consumption = df_MeterReading_NonSolar.merge(df_greenPercentages, left_on='Items_Timestamp_UTC', right_on='validfrom', how='left')
#     percentage_consumption['green_precentage_household'] = percentage_consumption['Items_ConsumptionDeliveryTotal']*percentage_consumption['Green_percentage_normalized']



