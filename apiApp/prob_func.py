#-------------------------PROBABILITY FUNCTION-------------------------------------
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import math 

    
def func(df):
    

    #df_engagement_client_data = pd.read_csv(file_name)
    df_engagement_client_data = df

    
    df_us_census_data = pd.read_csv('us_census_data.csv')

    df_engagement_model_data = df_engagement_client_data.merge(df_us_census_data, on = 'ZIP', how = 'left')


    df_engagement_model_data = df_engagement_model_data.rename(columns = {'__Black_or_African_American_alone':'per_black',
                                                                        '__Asian':'per_asian',
                                                                        '__With_a_disability':'per_with_disability',
                                                                        '__Worked_full-time,_year_round':'per_worked_ft',
                                                                        '__Worked_less_than_full-time,_year_round':'per_worked_lt_ft',
                                                                        '__household_population!!Below_$25,000':'hinc_below_25k',
                                                                        '__household_population!!$25,000_to_$49,999':'hinc_25k_to_50k',
                                                                        '__household_population!!$50,000_to_$74,999':'hinc_50k_to_75k',
                                                                        'Estimate__Percent_Insured_19_to':'per_ins_19_64',
                                                                        'Percent_Insured_AGE_55_to_64_yea':'per_ins_age_55_to_64',
                                                                        'Percent_Insured_Worked_full_time':'per_ins_worked_ft',
                                                                        'Insured__19_to_64_years!!Worked_less_than_full-time':'per_ins_19_64_worked_lt_ft',
                                                                        'Percent_Uninsured_19_to_25_years':'per_unins_19_25',
                                                                        'Percent_Uninsured_AGE_26_to_34_y':'per_unins_26_34',
                                                                        'Percent_Uninsured_AGE__45_to_54':'per_unins_45_54',
                                                                        'Percent_UninsuredAGE__55_to_64_y':'per_unins_55_64',
                                                                        'Percent_UninsuredAGE__19_to_64_y':'per_unins_19_64',
                                                                        'Percent_Uninsured_19_to_64_years':'per_unins_19_64_worked_lt_ft',
                                                                        '__Not_in_labor_force':'per_not_in_labor_force'})


    #Data Preparation

    df_engagement_model_data['per_not_in_labor_force'] = np.where(df_engagement_model_data.per_not_in_labor_force >=50,50,
                                                                np.where((df_engagement_model_data.per_not_in_labor_force >=30) & (df_engagement_model_data.per_not_in_labor_force <=50),30,df_engagement_model_data.per_not_in_labor_force))

    df_engagement_model_data['per_with_disability'] = np.where(df_engagement_model_data.per_with_disability >=30,30
                                                            ,df_engagement_model_data.per_with_disability)

    df_engagement_model_data['hinc_25k_to_50k'] = np.where(df_engagement_model_data.hinc_25k_to_50k >=40,40
                                                            ,df_engagement_model_data.hinc_25k_to_50k)

    df_engagement_model_data['hinc_50k_to_75k'] = np.where(df_engagement_model_data.hinc_50k_to_75k >=40,40
                                                            ,df_engagement_model_data.hinc_50k_to_75k)

    df_engagement_model_data['hinc_below_25k'] = np.where(df_engagement_model_data.hinc_below_25k >=40,40
                                                            ,df_engagement_model_data.hinc_below_25k)


    #State preparation

    df_engagement_model_data['d1_STATE'] = df_engagement_model_data[df_engagement_model_data.STATE == 'IN'].STATE
    df_engagement_model_data['d1_STATE'] = np.where(df_engagement_model_data['d1_STATE'].isna(),0,1)

    df_engagement_model_data['d2_STATE'] = df_engagement_model_data[df_engagement_model_data.STATE.isin(['CO','OH'])].STATE
    df_engagement_model_data['d2_STATE'] = np.where(df_engagement_model_data['d2_STATE'].isna(),0,1)

    df_engagement_model_data['d3_STATE'] = df_engagement_model_data[df_engagement_model_data.STATE == 'MO'].STATE
    df_engagement_model_data['d3_STATE'] = np.where(df_engagement_model_data['d3_STATE'].isna(),0,1)

    df_engagement_model_data['d4_STATE'] = df_engagement_model_data[df_engagement_model_data.STATE == 'NV'].STATE
    df_engagement_model_data['d4_STATE'] = np.where(df_engagement_model_data['d4_STATE'].isna(),0,1)

    #Region Preparation

    df_engagement_model_data['d2_REGION'] = df_engagement_model_data[df_engagement_model_data.REGION == 'Northeast'].REGION
    df_engagement_model_data['d2_REGION'] = np.where(df_engagement_model_data['d2_REGION'].isna(),0,1)

    df_engagement_model_data['d3_REGION'] = df_engagement_model_data[df_engagement_model_data.REGION == 'South'].REGION
    df_engagement_model_data['d3_REGION'] = np.where(df_engagement_model_data['d3_REGION'].isna(),0,1)

    #Age Data Preparation

    df_engagement_model_data['d1_AGE_O'] = df_engagement_model_data[df_engagement_model_data.AGE_ON_DEC20 <= 28].AGE_ON_DEC20
    df_engagement_model_data['d1_AGE_O'] = np.where(df_engagement_model_data['d1_AGE_O'].isna(),0,1)

    df_engagement_model_data['d2_AGE_O'] = df_engagement_model_data[(df_engagement_model_data.AGE_ON_DEC20 > 28) & (df_engagement_model_data.AGE_ON_DEC20 <= 47)].AGE_ON_DEC20
    df_engagement_model_data['d2_AGE_O'] = np.where(df_engagement_model_data['d2_AGE_O'].isna(),0,1)

    df_engagement_model_data['d3_AGE_O'] = df_engagement_model_data[(df_engagement_model_data.AGE_ON_DEC20 > 47) & (df_engagement_model_data.AGE_ON_DEC20 <= 59)].AGE_ON_DEC20
    df_engagement_model_data['d3_AGE_O'] = np.where(df_engagement_model_data['d3_AGE_O'].isna(),0,1)

    #Black and Asian Data Preparation

    df_engagement_model_data['d2_PER_BLACK'] = df_engagement_model_data[(df_engagement_model_data.per_black > 0.47) & (df_engagement_model_data.per_black <= 1.4)].per_black
    df_engagement_model_data['d2_PER_BLACK'] = np.where(df_engagement_model_data['d2_PER_BLACK'].isna(),0,1)

    df_engagement_model_data['d3_PER_ASIAN'] = df_engagement_model_data[(df_engagement_model_data.per_asian > 1.12) & (df_engagement_model_data.per_asian <= 3.03)].per_asian
    df_engagement_model_data['d3_PER_ASIAN'] = np.where(df_engagement_model_data['d3_PER_ASIAN'].isna(),0,1)


    #Estimated Population

    df_engagement_model_data['d3_Estimate'] = df_engagement_model_data[(df_engagement_model_data.Estimate__population > 16396) & (df_engagement_model_data.Estimate__population <= 30646)].Estimate__population
    df_engagement_model_data['d3_Estimate'] = np.where(df_engagement_model_data['d3_Estimate'].isna(),0,1)

    df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE'] = df_engagement_model_data[(df_engagement_model_data.per_not_in_labor_force <= 17.22)].per_not_in_labor_force
    df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE'] = np.where(df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE'].isna(),0,1)


    df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT'] = df_engagement_model_data[(df_engagement_model_data.per_ins_19_64_worked_lt_ft <= 80.5)].per_ins_19_64_worked_lt_ft
    df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT'] = np.where(df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT'].isna(),0,1)

    df_engagement_model_data['d1_PER_WORKED_FT'] = df_engagement_model_data[(df_engagement_model_data.per_worked_ft <= 58.96)].per_worked_ft
    df_engagement_model_data['d1_PER_WORKED_FT'] = np.where(df_engagement_model_data['d1_PER_WORKED_FT'].isna(),0,1)

    df_engagement_model_data['d1_PER_WITH_DISABILITY'] = df_engagement_model_data[(df_engagement_model_data.per_with_disability <= 9.28)].per_with_disability
    df_engagement_model_data['d1_PER_WITH_DISABILITY'] = np.where(df_engagement_model_data['d1_PER_WITH_DISABILITY'].isna(),0,1)

    #Household Inome data Preparation

    df_engagement_model_data['d1_HHINC_25K_TO_50K'] = df_engagement_model_data[(df_engagement_model_data.hinc_25k_to_50k <= 9.86)].hinc_25k_to_50k
    df_engagement_model_data['d1_HHINC_25K_TO_50K'] = np.where(df_engagement_model_data['d1_HHINC_25K_TO_50K'].isna(),0,1)

    df_engagement_model_data['d2_HHINC_25K_TO_50K'] = df_engagement_model_data[(df_engagement_model_data.hinc_25k_to_50k > 9.86) & (df_engagement_model_data.hinc_25k_to_50k <= 17.16)].hinc_25k_to_50k
    df_engagement_model_data['d2_HHINC_25K_TO_50K'] = np.where(df_engagement_model_data['d2_HHINC_25K_TO_50K'].isna(),0,1)

    df_engagement_model_data['d3_HHINC_25K_TO_50K'] = df_engagement_model_data[(df_engagement_model_data.hinc_25k_to_50k > 17.16) & (df_engagement_model_data.hinc_25k_to_50k <= 22.96)].hinc_25k_to_50k
    df_engagement_model_data['d3_HHINC_25K_TO_50K'] = np.where(df_engagement_model_data['d3_HHINC_25K_TO_50K'].isna(),0,1)

    df_engagement_model_data['d2_HHINC_50_TO_75K'] = df_engagement_model_data[(df_engagement_model_data.hinc_50k_to_75k > 12.32) & (df_engagement_model_data.hinc_50k_to_75k <= 17.74)].hinc_50k_to_75k
    df_engagement_model_data['d2_HHINC_50_TO_75K'] = np.where(df_engagement_model_data['d2_HHINC_50_TO_75K'].isna(),0,1)

    df_engagement_model_data['d3_HHINC_50_TO_75K'] = df_engagement_model_data[(df_engagement_model_data.hinc_50k_to_75k > 17.74) & (df_engagement_model_data.hinc_50k_to_75k <= 24.25)].hinc_50k_to_75k
    df_engagement_model_data['d3_HHINC_50_TO_75K'] = np.where(df_engagement_model_data['d3_HHINC_50_TO_75K'].isna(),0,1)

    df_engagement_model_data['d1_HHINC_BELOW_25K'] = df_engagement_model_data[(df_engagement_model_data.hinc_below_25k <= 4.91)].hinc_below_25k
    df_engagement_model_data['d1_HHINC_BELOW_25K'] = np.where(df_engagement_model_data['d1_HHINC_BELOW_25K'].isna(),0,1)

    df_engagement_model_data['d2_HHINC_BELOW_25K'] = df_engagement_model_data[(df_engagement_model_data.hinc_below_25k > 4.91) & (df_engagement_model_data.hinc_below_25k <= 11.48)].hinc_below_25k
    df_engagement_model_data['d2_HHINC_BELOW_25K'] = np.where(df_engagement_model_data['d2_HHINC_BELOW_25K'].isna(),0,1)


    Contract_Type = 'FF & Near Site'

    if Contract_Type == 'FF & Near Site':
        df_engagement_model_data['d1_Contract_Type'] = 1
        df_engagement_model_data['d2_Contract_Type'] = 0
        df_engagement_model_data['d4_Contract_Type'] = 0
        df_engagement_model_data['score'] = -0.6923-0.1696*df_engagement_model_data['d1_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-1.1351*df_engagement_model_data['d2_REGION']+0.2374*df_engagement_model_data['d3_REGION']-0.4876*df_engagement_model_data['d1_AGE_O']+0.2411*df_engagement_model_data['d2_AGE_O']+0.2971*df_engagement_model_data['d3_AGE_O']-0.117*df_engagement_model_data['d2_PER_BLACK']-0.1393*df_engagement_model_data['d3_PER_ASIAN']+0.0638*df_engagement_model_data['d3_Estimate']+0.2138*df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE']-0.1564*df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT']-0.3065*df_engagement_model_data['d1_PER_WORKED_FT']-0.1627*df_engagement_model_data['d1_PER_WITH_DISABILITY']-0.1854*df_engagement_model_data['d1_HHINC_25K_TO_50K']-0.1286*df_engagement_model_data['d2_HHINC_25K_TO_50K']-0.068*df_engagement_model_data['d3_HHINC_25K_TO_50K']+0.1218*df_engagement_model_data['d2_HHINC_50_TO_75K']+0.2493*df_engagement_model_data['d3_HHINC_50_TO_75K']+0.2997*df_engagement_model_data['d1_HHINC_BELOW_25K']+0.134*df_engagement_model_data['d2_HHINC_BELOW_25K']--0.4972*df_engagement_model_data['d1_Contract_Type']+0.3927*df_engagement_model_data['d2_Contract_Type']+0.335*df_engagement_model_data['d4_Contract_Type']
    elif Contract_Type == 'FF & On Site':
        df_engagement_model_data['d1_Contract_Type'] = 0
        df_engagement_model_data['d2_Contract_Type'] = 1
        df_engagement_model_data['d4_Contract_Type'] = 0
        df_engagement_model_data['score'] = -0.6923-0.1696*df_engagement_model_data['d1_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-1.1351*df_engagement_model_data['d2_REGION']+0.2374*df_engagement_model_data['d3_REGION']-0.4876*df_engagement_model_data['d1_AGE_O']+0.2411*df_engagement_model_data['d2_AGE_O']+0.2971*df_engagement_model_data['d3_AGE_O']-0.117*df_engagement_model_data['d2_PER_BLACK']-0.1393*df_engagement_model_data['d3_PER_ASIAN']+0.0638*df_engagement_model_data['d3_Estimate']+0.2138*df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE']-0.1564*df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT']-0.3065*df_engagement_model_data['d1_PER_WORKED_FT']-0.1627*df_engagement_model_data['d1_PER_WITH_DISABILITY']-0.1854*df_engagement_model_data['d1_HHINC_25K_TO_50K']-0.1286*df_engagement_model_data['d2_HHINC_25K_TO_50K']-0.068*df_engagement_model_data['d3_HHINC_25K_TO_50K']+0.1218*df_engagement_model_data['d2_HHINC_50_TO_75K']+0.2493*df_engagement_model_data['d3_HHINC_50_TO_75K']+0.2997*df_engagement_model_data['d1_HHINC_BELOW_25K']+0.134*df_engagement_model_data['d2_HHINC_BELOW_25K']--0.4972*df_engagement_model_data['d1_Contract_Type']+0.3927*df_engagement_model_data['d2_Contract_Type']+0.335*df_engagement_model_data['d4_Contract_Type']
    elif Contract_Type == 'PEPM & On Site':
        df_engagement_model_data['d1_Contract_Type'] = 0
        df_engagement_model_data['d2_Contract_Type'] = 0
        df_engagement_model_data['d4_Contract_Type'] = 1
        df_engagement_model_data['score'] = -0.6923-0.1696*df_engagement_model_data['d1_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-1.1351*df_engagement_model_data['d2_REGION']+0.2374*df_engagement_model_data['d3_REGION']-0.4876*df_engagement_model_data['d1_AGE_O']+0.2411*df_engagement_model_data['d2_AGE_O']+0.2971*df_engagement_model_data['d3_AGE_O']-0.117*df_engagement_model_data['d2_PER_BLACK']-0.1393*df_engagement_model_data['d3_PER_ASIAN']+0.0638*df_engagement_model_data['d3_Estimate']+0.2138*df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE']-0.1564*df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT']-0.3065*df_engagement_model_data['d1_PER_WORKED_FT']-0.1627*df_engagement_model_data['d1_PER_WITH_DISABILITY']-0.1854*df_engagement_model_data['d1_HHINC_25K_TO_50K']-0.1286*df_engagement_model_data['d2_HHINC_25K_TO_50K']-0.068*df_engagement_model_data['d3_HHINC_25K_TO_50K']+0.1218*df_engagement_model_data['d2_HHINC_50_TO_75K']+0.2493*df_engagement_model_data['d3_HHINC_50_TO_75K']+0.2997*df_engagement_model_data['d1_HHINC_BELOW_25K']+0.134*df_engagement_model_data['d2_HHINC_BELOW_25K']--0.4972*df_engagement_model_data['d1_Contract_Type']+0.3927*df_engagement_model_data['d2_Contract_Type']+0.335*df_engagement_model_data['d4_Contract_Type']
    else:
        df_engagement_model_data['d1_Contract_Type'] = 0
        df_engagement_model_data['d2_Contract_Type'] = 0
        df_engagement_model_data['d4_Contract_Type'] = 0
        df_engagement_model_data['score'] = -0.6923-0.1696*df_engagement_model_data['d1_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-0.72*df_engagement_model_data['d2_STATE']-3.1469*df_engagement_model_data['d3_STATE']+1.7295*df_engagement_model_data['d4_STATE']-1.1351*df_engagement_model_data['d2_REGION']+0.2374*df_engagement_model_data['d3_REGION']-0.4876*df_engagement_model_data['d1_AGE_O']+0.2411*df_engagement_model_data['d2_AGE_O']+0.2971*df_engagement_model_data['d3_AGE_O']-0.117*df_engagement_model_data['d2_PER_BLACK']-0.1393*df_engagement_model_data['d3_PER_ASIAN']+0.0638*df_engagement_model_data['d3_Estimate']+0.2138*df_engagement_model_data['d1_PER_NOT_IN_LABOUR_FORCE']-0.1564*df_engagement_model_data['d1_PER_INS_19_64_WORKED_LT_FT']-0.3065*df_engagement_model_data['d1_PER_WORKED_FT']-0.1627*df_engagement_model_data['d1_PER_WITH_DISABILITY']-0.1854*df_engagement_model_data['d1_HHINC_25K_TO_50K']-0.1286*df_engagement_model_data['d2_HHINC_25K_TO_50K']-0.068*df_engagement_model_data['d3_HHINC_25K_TO_50K']+0.1218*df_engagement_model_data['d2_HHINC_50_TO_75K']+0.2493*df_engagement_model_data['d3_HHINC_50_TO_75K']+0.2997*df_engagement_model_data['d1_HHINC_BELOW_25K']+0.134*df_engagement_model_data['d2_HHINC_BELOW_25K']--0.4972*df_engagement_model_data['d1_Contract_Type']+0.3927*df_engagement_model_data['d2_Contract_Type']+0.335*df_engagement_model_data['d4_Contract_Type']



    #-0.4972*df_engagement_model_data['d1_Contract_Type']+0.3927*df_engagement_model_data['d2_Contract_Type']+0.335*df_engagement_model_data['d4_Contract_Type']


    probab = []

    scores = df_engagement_model_data['score']

    for s in scores:
        probb = math.exp(-s)/(1+math.exp(-s))
        probab.append(probb)


    df_engagement_model_data['probability'] = probab

    return(df_engagement_model_data)
