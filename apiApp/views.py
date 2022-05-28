#-----------------------django modules-----------------------------------------------------------
from pydoc import doc
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.db.models import Avg
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat

#------------------------imported modules--------------------------------------------------------
from numpy import negative
import pandas as pd
import numpy as  np
import time
import datetime
from dateutil import rrule
import random
from operator import itemgetter
import re

#----------------------------models--------------------------------------------------------------
from apiApp.models import everside_clinic, everside_nps
#-------------------------Serializers------------------------------------------------------------
from apiApp.serializers import eversideAlertComments, eversideClient, eversideComments,eversideProviders
#----------------------------restAPI--------------------------------------------------------------
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser,FormParser

#---------------------Engagement Score Function---------------------------------------------------
from apiApp.prob_func import func




# Create your views here.
#Blog.objects.filter(pk__in=[1, 4, 7])
#---------------------------------------filter-----------------------------------------------------




@api_view(['GET'])
def filterRegion(request,format=None):
    try:
        if request.method == 'GET':
            frame = {'AL': 'Alabama',
                    'AK': 'Alaska',
                    'AZ': 'Arizona',
                    'AR': 'Arkansas',
                    'CA': 'California',
                    'CO': 'Colorado',
                    'CT': 'Connecticut',
                    'DE': 'Delaware',
                    'FL': 'Florida',
                    'GA': 'Georgia',
                    'HI': 'Hawaii',
                    'ID': 'Idaho',
                    'IL': 'Illinois',
                    'IN': 'Indiana',
                    'IA': 'Iowa',
                    'KS': 'Kansas',
                    'KY': 'Kentucky',
                    'LA': 'Louisiana',
                    'ME': 'Maine',
                    'MD': 'Maryland',
                    'MA': 'Massachusetts',
                    'MI': 'Michigan',
                    'MN': 'Minnesota',
                    'MS': 'Mississippi',
                    'MO': 'Missouri',
                    'MT': 'Montana',
                    'NE': 'Nebraska',
                    'NV': 'Nevada',
                    'NH': 'New Hampshire',
                    'NJ': 'New Jersey',
                    'NM': 'New Mexico',
                    'NY': 'New York',
                    'NC': 'North Carolina',
                    'ND': 'North Dakota',
                    'OH': 'Ohio',
                    'OK': 'Oklahoma',
                    'OR': 'Oregon',
                    'PA': 'Pennsylvania',
                    'RI': 'Rhode Island',
                    'SC': 'South Carolina',
                    'SD': 'South Dakota',
                    'TN': 'Tennessee',
                    'TX': 'Texas',
                    'UT': 'Utah',
                    'VT': 'Vermont',
                    'VA': 'Virginia',
                    'WA': 'Washington',
                    'WV': 'West Virginia',
                    'WI': 'Wisconsin',
                    'WY': 'Wyoming'}

            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400            
            region = []
            obj = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).exclude(state__isnull=True).exclude(state__exact='nan').values_list('state',flat=True).distinct()       
            for i in obj:
                region.append(str(frame[i])+','+str(i))
                
            region.sort()
        return Response({'Message':'TRUE','region':region})
    except:
        return Response({'Message':'FALSE'})



@api_view(['GET'])
def filterClinic(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = request.GET.get('region')
            region = re.split(r"-|,", region)
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400   
            obj = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).values_list('clinic',flat=True).distinct()    
            if '' not in region:
                # city = []
                # state = []
                # for i in region.split('-'):
                #     city.append(i.split(',')[0])
                #     state.append(i.split(',')[1])
                obj = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(state__in=region).values_list('clinic',flat=True).distinct()
            data = list(obj)
            data.sort()
        return Response({'Message':'TRUE','clinic':data,})
    except:
        return Response({'Message':'FALSE'})        




#--------------------------------------API Functions---------------------------------------------

@api_view(['POST'])
def userLogin(request,format=None):
    if request.method == 'POST':
        try:
            data = request.data
            username = str(data['username'])
            password = str(data['password'])
        
            if username == 'everside_user' or username == 'user@everside.com':
                if password == 'Test@1234':
                    return Response({'Message':'TRUE'})
                else:
                    return Response({'Message':'FALSE'})
            elif username=='a':
                if password=='a':
                    return Response({'Message':'TRUE'})
                else:
                    return Response({'Message':'FALSE'})
            else:
                return Response({'Message':'FALSE'})
        except:
            return Response({'Message':'FALSE'})
            

#---------------------------Dashboard Api's------------------------------------------------------

@api_view(['GET'])
def netPromoterScore(request,format=None):
    if request.method == 'GET':
        # try:
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)       
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400
            total_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).values()
            promoters_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(nps_label = 'Promoter').values()
            passive_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(nps_label = 'Passive').values()
            detractors_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(nps_label = 'Detractor').values()
            if '' not in region:
                # for i in region:
                #     city.append(i.split(',')[0])
                #     state.append(i.split(',')[1])
                total_count = total_count.filter(state__in = region)
                promoters_count = promoters_count.filter(state__in = region)
                passive_count = passive_count.filter(state__in = region)
                detractors_count = detractors_count.filter(state__in = region)
            if '' not in clinic:
                total_count = total_count.filter(clinic__in = clinic)
                promoters_count = promoters_count.filter(clinic__in = clinic)
                passive_count = passive_count.filter(clinic__in = clinic)
                detractors_count = detractors_count.filter(clinic__in = clinic)
            
            if(len(promoters_count)>0):
                    promoters = round(len(promoters_count)/len(total_count)*100)
                    if promoters == 0:
                        promoters = round(len(promoters_count)/len(total_count)*100,2)
            else:
                promoters = 0     

            if(len(passive_count)>0):
                    passive = round(len(passive_count)/len(total_count)*100)
                    if passive == 0:
                        passive = round(len(passive_count)/len(total_count)*100,2)
            else:
                passive = 0      

            if(len(detractors_count)>0):
                    detractors = round(len(detractors_count)/len(total_count)*100)
                    if detractors == 0:
                        detractors = round(len(detractors_count)/len(total_count)*100,2)
            else:
                detractors = 0      
            
            nps ={
                    "nps_score":(promoters-detractors-passive),
                    "promoters":promoters,
                    "total_promoters":len(promoters_count),
                    "passive":passive,
                    "total_passive":len(passive_count),
                    "detractors":detractors,
                    "total_detractors":len(detractors_count),
                }

            nps_pie = [{
                            "label":"Promoters",
                            "percentage":promoters,
                            "color":"#00AC69",
                        },
                        {
                            "label":"Passives",
                            "percentage":passive,
                            "color":"#939799",
                        },
                        {
                            "label":"Detractors",
                            "percentage":detractors,
                            "color":"#DB2B39",
                        }]

            return Response({'Message':'TRUE',
                                'nps':nps,
                                'nps_pie':nps_pie})

        # except:
        #     return Response({'Message':'FALSE'})
            
            

@api_view(['GET'])
def netSentimentScore(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400
            total_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).values()
            positive_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Positive').values()
            negative_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Negative').values()
            extreme_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Extreme').values()

            state = region
            if '' not in region:
                # for i in region:
                #     city.append(i.split(',')[0])
                #     state.append(i.split(',')[1])
                total_count = total_count.filter(state__in = state)
                positive_count = positive_count.filter(state__in = state)
                negative_count = negative_count.filter(state__in = state)
                extreme_count = extreme_count.filter(state__in = state)
            
            if '' not in clinic:
                total_count = total_count.filter(clinic__in = clinic)
                positive_count = positive_count.filter(clinic__in = clinic)
                negative_count = negative_count.filter(clinic__in = clinic)
                extreme_count = extreme_count.filter(clinic__in = clinic)
            
            if(len(positive_count)!=0):
                positive = round(len(positive_count)/len(total_count)*100)
                if positive == 0:
                    positive = round(len(positive_count)/len(total_count)*100,2)
            else:
                positive = 0
            
            if(len(negative_count)!=0):
                negative = round(len(negative_count)/len(total_count)*100)
                if negative == 0:
                    negative = round(len(negative_count)/len(total_count)*100,2)
            else:
                negative = 0
            
            if(len(extreme_count)!=0):
                extreme = round(len(extreme_count)/len(total_count)*100)
                if extreme == 0:
                    extreme = round(len(extreme_count)/len(total_count)*100,2)
            else:
                extreme = 0

            nss ={
                    "nss_score":(positive-negative-extreme),
                    "total": len(total_count),
                    "positive":positive,
                    "total_positive":len(positive_count),
                    "negative":negative,
                    "total_negative":len(negative_count),
                    "extreme":extreme,
                    "total_extreme":len(extreme_count),
                }
                
            nss_pie = [{
                        "label":"Positive",
                        "percentage":positive,
                        "color":"#00AC69",
                    },
                    {
                        "label":"Negative",
                        "percentage":negative,
                        "color":"#ffa500",
                    },
                    {
                        "label":"Extreme",
                        "percentage":extreme,
                        "color":"#DB2B39",
                    }]
            return Response({'Message':'TRUE',
                             'nss':nss,
                             'nss_pie':nss_pie})
    except:
        return Response({'Message':'FALSE'})

@api_view(['GET'])
def npsOverTime(request,format=None):
    try:
        if request.method == 'GET':
            months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)   
            nps_over_time = []
            start_date = datetime.datetime(int(start_year),int(start_month) , 1)
            end_date = datetime.datetime(int(end_year),int(end_month), 1)
            for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
                start_date = str(dt.month)+'-'+str(dt.year)
                startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
                if dt.month < 12:
                    end_date = str(dt.month + 1)+'-'+str(dt.year)
                else:
                    end_date = str('1-')+str(int(end_year)+1)
                    
                endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400
                total_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).values()
                promoters_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(nps_label = 'Promoter').values()
                passive_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(nps_label = 'Passive').values()
                detractors_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(nps_label = 'Detractor').values()
                state = region
                if '' not in region:
                    # for i in region:
                    #     city.append(i.split(',')[0])
                    #     state.append(i.split(',')[1])
                    total_count = total_count.filter(state__in = state)
                    promoters_count = promoters_count.filter(state__in = state)
                    passive_count = passive_count.filter(state__in = state)
                    detractors_count = detractors_count.filter(state__in = state)
            
                if '' not in clinic:
                    total_count = total_count.filter(clinic__in = clinic)
                    promoters_count = promoters_count.filter(clinic__in = clinic)
                    passive_count = passive_count.filter(clinic__in = clinic)
                    detractors_count = detractors_count.filter(clinic__in = clinic)
                if(len(promoters_count)!=0):
                        promoters = round(len(promoters_count)/len(total_count)*100)
                        if promoters == 0:
                            promoters = round(len(promoters_count)/len(total_count)*100,2)
                else:
                    promoters = 0     

                if(len(passive_count)!=0):
                        passive = round(len(passive_count)/len(total_count)*100)
                        if passive == 0:
                            passive = round(len(passive_count)/len(total_count)*100,2)
                else:
                    passive = 0      

                if(len(detractors_count)!=0):
                        detractors = round(len(detractors_count)/len(total_count)*100)
                        if detractors == 0:
                            detractors = round(len(detractors_count)/len(total_count)*100,2)
                else:
                    detractors = 0      
                nps = (int(promoters-detractors-passive))
                if(nps<0):
                    nps = 0
                over_time_data = {
                        'month': str(months[dt.month - 1]),
                        'year': dt.year,
                        'nps': nps,
                        'promoter':promoters,
                        'passive':passive,
                        'detractor':detractors,
                    }
                nps_over_time.append(over_time_data)
        return Response({'Message':'TRUE','nps_over_time':nps_over_time})
    except:
        return Response({'Message':'FALSE'})


@api_view(['GET'])
def nssOverTime(request,format=None):
    try:
        if request.method == 'GET':
            months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            nss_over_time = []
            start_date = datetime.datetime(int(start_year),int(start_month) , 1)
            end_date = datetime.datetime(int(end_year),int(end_month), 1)
            for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
                start_date = str(dt.month)+'-'+str(dt.year)
                startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
                if dt.month < 12:
                    end_date = str(dt.month + 1)+'-'+str(dt.year)
                else:
                    end_date = str('1-')+str(int(end_year)+1)
                    
                endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400
                total_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).values()
                positive_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label = 'Positive').values()
                negative_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label = 'Negative').values()
                neutral_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label = 'Neutral').values()
                extreme_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label = 'Extreme').values()
                # city = []
                state = region
                if '' not in region:
                    # for i in region:
                    #     city.append(i.split(',')[0])
                    #     state.append(i.split(',')[1])
                    total_count = total_count.filter(state__in = state)
                    positive_count = positive_count.filter(state__in = state)
                    negative_count = negative_count.filter(state__in = state)
                    neutral_count = neutral_count.filter(state__in = state)
                    extreme_count = extreme_count.filter(state__in = state)
                
                if '' not in clinic:
                    total_count = total_count.filter(clinic__in = clinic)
                    positive_count = positive_count.filter(clinic__in = clinic)
                    negative_count = negative_count.filter(clinic__in = clinic)
                    neutral_count = neutral_count.filter(clinic__in = clinic)
                    extreme_count = extreme_count.filter(clinic__in = clinic)
                if(len(positive_count)!=0):
                    positive = round(len(positive_count)/len(total_count)*100)
                    if positive == 0:
                        positive = round(len(positive_count)/len(total_count)*100,2)
                else:
                    positive = 0
                
                if(len(negative_count)!=0):
                    negative = round(len(negative_count)/len(total_count)*100)
                    if negative == 0:
                        negative = round(len(negative_count)/len(total_count)*100,2)
                else:
                    negative = 0
                
                if(len(neutral_count)!=0):
                    neutral = round(len(neutral_count)/len(total_count)*100)
                    if neutral == 0:
                        neutral = round(len(neutral_count)/len(total_count)*100,2)
                else:
                    neutral = 0
                
                if(len(extreme_count)!=0):
                    extreme = round(len(extreme_count)/len(total_count)*100)
                    if extreme == 0:
                        extreme = round(len(extreme_count)/len(total_count)*100,2)
                else:
                    extreme = 0
                nss = (int(positive-negative-extreme))
                if (nss<0):
                    nss = 0
                over_time_data = {
                            'month': str(months[dt.month-1]),
                            'year': dt.year,
                            'nss': nss,
                            'positive':positive,
                            'negative':negative,
                            'extreme':extreme,
                            'neutral':neutral,
                        }
                nss_over_time.append(over_time_data)
        return Response({'Message':'TRUE','nss_over_time':nss_over_time})
    except:
        return Response({'Message':'FALSE'})

@api_view(['GET'])
def npsVsSentiments(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400
            #-------------Extreme----------------------------------------------------------------
            extreme_total_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Extreme').values()
            extreme_promoters_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Extreme').filter(nps_label='Promoter').values()
            extreme_passive_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Extreme').filter(nps_label='Passive').values()
            extreme_detractors_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Extreme').filter(nps_label = 'Detractor').values()
            state = region
            if '' not in region:
                # for i in region:
                #     city.append(i.split(',')[0])
                #     state.append(i.split(',')[1])
                extreme_total_count = extreme_total_count.filter(state__in = state)
                extreme_promoters_count = extreme_promoters_count.filter(state__in = state)
                extreme_passive_count = extreme_passive_count.filter(state__in = state)
                extreme_detractors_count = extreme_detractors_count.filter(state__in = state)
            
            if '' not in clinic:
                extreme_total_count = extreme_total_count.filter(clinic__in = clinic)
                extreme_promoters_count = extreme_promoters_count.filter(clinic__in = clinic)
                extreme_passive_count = extreme_passive_count.filter(clinic__in = clinic)
                extreme_detractors_count = extreme_detractors_count.filter(clinic__in = clinic)
            
            if len(extreme_promoters_count)!=0:
                    extreme_promoters = round(len(extreme_promoters_count)/len(extreme_total_count)*100)
                    if extreme_promoters == 0:
                        extreme_promoters = round(len(extreme_promoters_count)/len(extreme_total_count)*100,2)
            else:
                extreme_promoters = 0 
            if len(extreme_passive_count)!=0:
                    extreme_passive = round(len(extreme_passive_count)/len(extreme_total_count)*100)
                    if extreme_passive == 0:
                        extreme_passive = round(len(extreme_passive_count)/len(extreme_total_count)*100,2)
            else:
                extreme_passive = 0
            if len(extreme_detractors_count)!=0:
                    extreme_detractors = round(len(extreme_detractors_count)/len(extreme_total_count)*100)
                    if extreme_detractors == 0:
                        extreme_detractors = round(len(extreme_detractors_count)/len(extreme_total_count)*100,2)
            else:
                extreme_detractors = 0

            extreme = {
                    'sentiment_label':'Extreme',
                    'promoter':extreme_promoters,
                    'passive':extreme_passive,
                    'detractor':extreme_detractors,
                }
            
            #-------------Positive---------------------------------------------------------------
            positive_total_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Positive').values()
            positive_promoters_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Positive').filter(nps_label='Promoter').values()
            positive_passive_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Positive').filter(nps_label='Passive').values()
            positive_detractors_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Positive').filter(nps_label='Detractor').values()
            # city = []
            state = region
            if '' not in region:
            #     for i in region:
            #         city.append(i.split(',')[0])
            #         state.append(i.split(',')[1])
                positive_total_count = positive_total_count.filter(state__in = state)
                positive_promoters_count = positive_promoters_count.filter(state__in = state)
                positive_passive_count = positive_passive_count.filter(state__in = state)
                positive_detractors_count = positive_detractors_count.filter(state__in = state)
            
            if '' not in clinic:
                positive_total_count = positive_total_count.filter(clinic__in = clinic)
                positive_promoters_count = positive_promoters_count.filter(clinic__in = clinic)
                positive_passive_count = positive_passive_count.filter(clinic__in = clinic)
                positive_detractors_count = positive_detractors_count.filter(clinic__in = clinic)

            if len(positive_promoters_count)!=0:
                    positive_promoters = round(len(positive_promoters_count)/len(positive_total_count)*100)
                    if positive_promoters == 0:
                        positive_promoters = round(len(positive_promoters_count)/len(positive_total_count)*100,2)
            else:
                positive_promoters = 0 
            if len(positive_passive_count)!=0:
                    positive_passive = round(len(positive_passive_count)/len(positive_total_count)*100)
                    if positive_passive == 0:
                        positive_passive = round(len(positive_passive_count)/len(positive_total_count)*100,2)
            else:
                positive_passive = 0
            if len(positive_detractors_count)!=0:
                    positive_detractors = round(len(positive_detractors_count)/len(positive_total_count)*100)
                    if positive_detractors == 0:
                        positive_detractors = round(len(positive_detractors_count)/len(positive_total_count)*100,2)
            else:
                positive_detractors = 0

            positive = {
                    'sentiment_label':'positive',
                    'promoter':positive_promoters,
                    'passive':positive_passive,
                    'detractor':positive_detractors,
                }
            #-------------Negative---------------------------------------------------------------
            negative_total_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Negative').values()
            negative_promoters_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Negative').filter(nps_label='Promoter').values()
            negative_passive_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Negative').filter(nps_label='Passive').values()
            negative_detractors_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Negative').filter(nps_label='Detractor').values()
            # city = []
            state = region
            if '' not in region:
                # for i in region:
                #     city.append(i.split(',')[0])
                #     state.append(i.split(',')[1])
                negative_total_count = negative_total_count.filter(state__in = state)
                negative_promoters_count = negative_promoters_count.filter(state__in = state)
                negative_passive_count = negative_passive_count.filter(state__in = state)
                negative_detractors_count = negative_detractors_count.filter(state__in = state)
            
            if '' not in clinic:
                negative_total_count = negative_total_count.filter(clinic__in = clinic)
                negative_promoters_count = negative_promoters_count.filter(clinic__in = clinic)
                negative_passive_count = negative_passive_count.filter(clinic__in = clinic)
                negative_detractors_count = negative_detractors_count.filter(clinic__in = clinic)

            if len(negative_promoters_count)!=0:
                    negative_promoters = round(len(negative_promoters_count)/len(negative_total_count)*100)
                    if negative_promoters == 0:
                        negative_promoters = round(len(negative_promoters_count)/len(negative_total_count)*100,2)
            else:
                negative_promoters = 0 
            if len(negative_passive_count)!=0:
                    negative_passive = round(len(negative_passive_count)/len(negative_total_count)*100)
                    if negative_passive == 0:
                        negative_passive = round(len(negative_passive_count)/len(negative_total_count)*100,2)
            else:
                negative_passive = 0
            if len(negative_detractors_count)!=0:
                    negative_detractors = round(len(negative_detractors_count)/len(negative_total_count)*100)
                    if negative_detractors == 0:
                        negative_detractors = round(len(negative_detractors_count)/len(negative_total_count)*100,2)
            else:
                negative_detractors = 0

            negative = {
                    'sentiment_label':'negative',
                    'promoter':negative_promoters,
                    'passive':negative_passive,
                    'detractor':negative_detractors,
                }
            #-------------Neutral----------------------------------------------------------------
            neutral_total_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Neutral').values()
            neutral_promoters_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Neutral').filter(nps_label='Promoter').values()
            neutral_passive_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Neutral').filter(nps_label='Passive').values()
            neutral_detractors_count = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Neutral').filter(nps_label='Detractor').values()
            # city = []
            state = region
            if '' not in region:
                # for i in region:
                #     city.append(i.split(',')[0])
                #     state.append(i.split(',')[1])
                neutral_total_count = neutral_total_count.filter(state__in = state)
                neutral_promoters_count = neutral_promoters_count.filter(state__in = state)
                neutral_passive_count = neutral_passive_count.filter(state__in = state)
                neutral_detractors_count = neutral_detractors_count.filter(state__in = state)
            
            if '' not in clinic:
                neutral_total_count = neutral_total_count.filter(clinic__in = clinic)
                neutral_promoters_count = neutral_promoters_count.filter(clinic__in = clinic)
                neutral_passive_count = neutral_passive_count.filter(clinic__in = clinic)
                neutral_detractors_count = neutral_detractors_count.filter(clinic__in = clinic)
            if len(neutral_promoters_count)!=0:
                    neutral_promoters = round(len(neutral_promoters_count)/len(neutral_total_count)*100)
                    if neutral_promoters == 0:
                        neutral_promoters = round(len(neutral_promoters_count)/len(neutral_total_count)*100,2)
            else:
                neutral_promoters = 0 
            if len(neutral_passive_count)!=0:
                    neutral_passive = round(len(neutral_passive_count)/len(neutral_total_count)*100)
                    if neutral_passive == 0:
                        neutral_passive = round(len(neutral_passive_count)/len(neutral_total_count)*100,2)
            else:
                neutral_passive = 0
            if len(neutral_detractors_count)!=0:
                    neutral_detractors = round(len(neutral_detractors_count)/len(neutral_total_count)*100)
                    if neutral_detractors == 0:
                        neutral_detractors = round(len(neutral_detractors_count)/len(neutral_total_count)*100,2)
            else:
                neutral_detractors = 0

            neutral = {
                    'sentiment_label':'neutral',
                    'promoter':neutral_promoters,
                    'passive':neutral_passive,
                    'detractor':neutral_detractors,
                }
            final_data = [extreme,negative,neutral,positive]
        return Response({'Message':'TRUE','data':final_data})
    except:
        return Response({'Message':'FALSE'})
        

@api_view(['GET'])
def alertComments(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400
            alert_comments = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Extreme').order_by('-timestamp').values()
            # city = []
            state = region
            if '' not in region:
                # for i in region:
                #     city.append(i.split(',')[0])
                #     state.append(i.split(',')[1])
                alert_comments = alert_comments.filter(state__in = state)
            if '' not in clinic:
                alert_comments = alert_comments.filter(clinic__in = clinic)
            serialized_alert_comments = eversideAlertComments(alert_comments,many=True)
        return Response({'Message':'TRUE','data':serialized_alert_comments.data})
    except:
        return Response({'Message':'FALSE'})


@api_view(['GET'])
def topComments(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400
            positive = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Positive').order_by('?').values()
            negative = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Negative').order_by('?').values()
            neutral = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Neutral').order_by('?').values()
            extreme = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Extreme').order_by('?').values()
            # city = []
            state = region
            if '' not in region:
                # for i in region:
                #     city.append(i.split(',')[0])
                #     state.append(i.split(',')[1])
                positive = positive.filter(state__in = state)
                negative = negative.filter(state__in = state)
                neutral = neutral.filter(state__in = state)
                extreme = extreme.filter(state__in = state)

            if '' not in clinic:
                positive = positive.filter(clinic__in = clinic)
                negative = negative.filter(clinic__in = clinic)
                neutral = neutral.filter(clinic__in = clinic)
                extreme = extreme.filter(clinic__in = clinic)
            top_comments = list(positive[:4])+list(negative[:4])+list(extreme[:4])+list(neutral[:4])
            random.shuffle(top_comments)
            serialized_top_comments = eversideComments(top_comments,many=True)
        return Response({'Message':'TRUE','data':serialized_top_comments.data})
    except:
        return Response({'Message':'FALSE'})

@api_view(['GET'])
def totalComments(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400 
            all_comments = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).order_by('-timestamp').values()
            # city = []
            state = region
            if '' not in region:
                # for i in region:
                #     city.append(i.split(',')[0])
                #     state.append(i.split(',')[1])
                all_comments = all_comments.filter(state__in = state)
            if '' not in clinic:
                all_comments = all_comments.filter(clinic__in = clinic)
            serialized_all_comments = eversideComments(all_comments,many=True)
        return Response({'Message':'TRUE','data':serialized_all_comments.data})
    except:
        return Response({'Message':'FALSE'})

@api_view(['GET'])
def clinicData(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400 
            clinic_list = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).values_list('clinic','city','state').distinct()
            # city = []
            state = region
            if '' not in region:
                # for i in region:
                #     city.append(i.split(',')[0])
                #     state.append(i.split(',')[1])
                clinic_list = clinic_list.filter(state__in = state)
            if '' not in clinic:
                clinic_list = clinic_list.filter(clinic__in = clinic)
            clinic_data = []
            for i in list(clinic_list):
                nps_score = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(clinic = i[0]).aggregate(Avg('nps_score'))
                data = {'clinic':i[0],
                        'city':i[1],
                        'state':i[2],
                        'nps':round(nps_score['nps_score__avg'],2)}
                clinic_data.append(data)
            
            clinic_data = sorted(clinic_data, key=itemgetter('nps'))
        return Response({'Message':'TRUE','data':clinic_data[::-1]})
    except:
        return Response({'Message':'FALSE'})       

@api_view(['GET'])
def totalCards(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400 
            comments = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).values_list('review')
            survey = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).values_list('review_id').distinct()
            alerts = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).filter(label='Extreme')
            clinics = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).values_list('clinic').distinct()
            doctors = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).values_list('provider_name').distinct()
            clients = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).exclude(client_name__isnull=True).exclude(client_name__exact='nan').values_list('client_id').distinct()
            # city = []
            state = region
            if '' not in region:
                # for i in region:
                #     city.append(i.split(',')[0])
                #     state.append(i.split(',')[1])
                comments = comments.filter(state__in = state)
                survey = survey.filter(state__in = state)
                alerts = alerts.filter(state__in = state)
                clinics = clinics.filter(state__in = state)
                doctors = doctors.filter(state__in = state)
                clients = clients.filter(state__in = state)

            if '' not in clinic:
                comments = comments.filter(clinic__in = clinic)
                survey = survey.filter(clinic__in = clinic)
                alerts = alerts.filter(clinic__in = clinic)
                clinics = clinics.filter(clinic__in = clinic)
                doctors = doctors.filter(clinic__in = clinic)
                clients = clients.filter(clinic__in = clinic)
            comments = comments 
            survey = survey
            alerts = alerts
            clinics = clinics
            card_data = {
                            'survey':len(survey),
                            'comments': len(comments),
                            'alerts': len(alerts),
                            'clinic': len(clinics),
                            'doctors':len(doctors),
                            'clients':len(clients),
                    }
        return Response({'Message':'TRUE','card_data':card_data})
    except:
        return Response({'Message':'FALSE'})     

@api_view(['GET'])
def providersData(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400 
            providers = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).values('provider_name','provider_type','provider_category').exclude(provider_type__isnull=True).exclude(provider_type__exact='').distinct()
            state = region
            if '' not in region:
                providers = providers.filter(state__in = state)
            if '' not in clinic:
                providers = providers.filter(clinic__in = clinic)
            serialized_providers = eversideProviders(providers,many=True)
        return Response({'Message':'TRUE','data':serialized_providers.data})
    except:
        return Response({'Message':'FALSE'})       

@api_view(['GET'])
def clientData(request,format=None):
    try:
        if request.method == 'GET':
            start_year = request.GET.get('start_year')
            start_month = request.GET.get('start_month')
            end_year = request.GET.get('end_year')
            end_month = request.GET.get('end_month')
            region = (request.GET.get('region'))
            clinic = (request.GET.get('clinic'))
            region = re.split(r"-|,", region)
            clinic = re.split(r"-|,", clinic)  
            start_date = str(start_month)+'-'+str(start_year)
            startDate = (time.mktime(datetime.datetime.strptime(start_date,"%m-%Y").timetuple()))
            if int(end_month)<12:
                end_date = str(int(end_month)+1)+'-'+str(end_year)
            else:
                end_date = str('1-')+str(int(end_year)+1)
            endDate = (time.mktime(datetime.datetime.strptime(end_date,"%m-%Y").timetuple())) - 86400 
            client = everside_nps.objects.filter(timestamp__gte=startDate).filter(timestamp__lte=endDate).exclude(client_name__isnull=True).exclude(client_name__exact='nan').values("client_name","parent_client_name").distinct()
            state = region
            if '' not in region:
                client = client.filter(state__in = state)
            if '' not in clinic:
                client = client.filter(clinic__in = clinic)
            serialized_client = eversideClient(client,many=True)
        return Response({'Message':'TRUE','data':serialized_client.data})
    except:
        return Response({'Message':'FALSE'})     
#---------------------------Engagement Score Api-------------------------------------------------
@api_view(['POST'])
@parser_classes([MultiPartParser,FormParser])
def egStatistics(request,format=None):
    try:
        up_file = request.FILES.getlist('file')

        df = pd.read_csv(up_file[0])
        if 'CLIENT_ID' in list(df.columns) and "MEMBER_ID" in list(df.columns) and 'ZIP' in df.columns and 'HOUSEHOLD_ID' in list(df.columns):
            mes = 'TRUE'

        else:
            mes = 'FALSE'
        return Response({'Message':mes,'rows':df.shape[0],'columns':df.shape[1]})

    except:
        return Response({'Message':"FALSE",'ERROR':'INCORRECT FILE TYPE'})



@api_view(['POST'])
@parser_classes([MultiPartParser,FormParser])
def egPercentileMember(request,format=None):
    try:
        up_file = request.FILES.getlist('file')
        df = pd.read_csv(up_file[0])
        out = func(df)
        out_prob = list(out['probability'])
        low = 0 # n < 0.5
        med = 0 # 0.5 < n < 0.75
        high = 0 # 0.75 < n
        graph = [] 
        p_values = [0,1,25,33,50,66,75,95,99,100]
        for i in p_values:
            p = np.percentile(out_prob,i)
            percentile_name = "P"+str(i)
            percentile_value = round(p,3)
            member_score = out_prob.count(p)
            if p < 0.5:
                low = low + 1
            elif 0.5 <= p < 0.75:
                med = med + 1
            else:
                high = high + 1

            frame = {
                'percentile_name':percentile_name,
                'percentile_value':percentile_value,
                'member_score':member_score
            }
            graph.append(frame)
            percentage = {
                'low':str(low*10)+"%",
                'medium':str(low*10+med*10)+"%",
                'high':'100%',
            }


        return Response({'Message':'TRUE','graph':graph,'percentage':percentage})

    except:
        return Response({'Message':"FALSE"})


# def index(request):
#     # everside_nps.objects.all().delete()
# #     everside_nps.objects.filter(nps_label = 'Detractors').update(nps_label = 'Detractor')
    
# #     # everside_nps.objects.all().delete()
#     df = pd.read_csv('final_wdw.csv')
#     for i in range(df.shape[0]):
#         a = (time.mktime(datetime.datetime.strptime((list(df['SURVEY_MONTH']))[i],"%b-%y").timetuple()))
#         # review_id = list(df['ID'])[i]
#         # review = list(df['reviews'])[i]
#         # date = list(df['SURVEYDATE__C'])[i]
#         # nps_score = list(df['NPS'])[i]
#         # clinic = list(df['NPSCLINIC__C'])[i]
#         # city = list(df['CLINIC_CITY'])[i]
#         # state = list(df['CLINIC_STATE'])[i]
#         # polarity_score = list(df['polarity_score'])[i]
#         # label = list(df['sentiment_label'])[i]
#         # nps_label = list(df['nps_label'])[i]
#         # timestamp = a
#         # member_id = list(df['MEMBER_ID'])[i]
#         # survey_date = list(df['SURVEYDATE__C'])[i]
#         # survey_month = list(df['SURVEY_MONTH'])[i]
#         # survey_year = list(df['SURVEY_YEAR'])[i]
#         # survey_number = list(df['SURVEYNUMBER__C'])[i]
#         # clinic_id = list(df['CLINIC_ID'])[i]
#         # clinic_street = list(df['CLINIC_STREET'])[i]
#         # clinic_city = list(df['CLINIC_CITY'])[i]
#         # clinic_state = list(df['CLINIC_STATE'])[i]
#         # clinic_zip = list(df['CLINIC_ZIP'])[i]
#         # clinic_type = list(df['CLINIC_TYPE'])[i]
#         # provider_name = list(df['PROVIDER_NAME'])[i]
#         # provider_type = list(df['PROVIDERTYPE__C'])[i]
#         # provider_category = list(df['PROVIDER_CATEGORY__C'])[i]
#         # client_naics = list(df['CLIENT_NAICS'])[i]
#         # client_id = list(df['CLIENT_ID'])[i]
#         # client_name = list(df['CLIENT NAME'])[i]
#         # parent_client_id = list(df['PARENT_CLIENT_ID'])[i]
#         # parent_client_name = list(df['PARENT CLIENT NAME'])[i]
#         # question_type = list(df['question_type'])[i]
#         # print('review_id',review_id)
#         # print('review',review)
#         # print('date',date)
#         # print('nps_score',nps_score)
#         # print('clinic',clinic)
#         # print('city',city)
#         # print('state',state)
#         # print('polarity_score',polarity_score)
#         # print('label',label)
#         # print('nps_label',nps_label)
#         # print('timestamp',timestamp)
#         # print('member_id',member_id)
#         # print('survey_date',survey_date)
#         # print('survey_month',survey_month)
#         # print('survey_year',survey_year)
#         # print('survey_number',survey_number)
#         # print('clinic_id',clinic_id)
#         # print('clinic_street',clinic_street)
#         # print('clinic_city',clinic_city)
#         # print('clinic_state',clinic_state)
#         # print('clinic_zip',clinic_zip)
#         # print('clinic_type',clinic_type)
#         # print('provider_name',provider_name)
#         # print('provider_type',provider_type)
#         # print('provider_category',provider_category)
#         # print('client_naics',client_naics)
#         # print('client_id',client_id)
#         # print('client_name',client_name)
#         # print('parent_client_id',parent_client_id)
#         # print('parent_client_name',parent_client_name)
#         # print('question_type',question_type)
#         data = everside_nps(review_id = list(df['ID'])[i],
#                             review = list(df['reviews'])[i],
#                             date = list(df['SURVEYDATE__C'])[i],
#                             nps_score = list(df['NPS'])[i],
#                             clinic = list(df['NPSCLINIC__C'])[i],
#                             city = list(df['CLINIC_CITY'])[i],
#                             state = list(df['CLINIC_STATE'])[i],
#                             polarity_score = list(df['polarity_score'])[i],
#                             label = list(df['sentiment_label'])[i],
#                             nps_label = list(df['nps_label'])[i],
#                             timestamp = a,
#                             member_id = list(df['MEMBER_ID'])[i],
#                             survey_date = list(df['SURVEYDATE__C'])[i],
#                             survey_month = list(df['SURVEY_MONTH'])[i],
#                             survey_year = list(df['SURVEY_YEAR'])[i],
#                             survey_number = list(df['SURVEYNUMBER__C'])[i],
#                             clinic_id = list(df['CLINIC_ID'])[i],
#                             clinic_street = list(df['CLINIC_STREET'])[i],
#                             clinic_city = list(df['CLINIC_CITY'])[i],
#                             clinic_state = list(df['CLINIC_STATE'])[i],
#                             clinic_zip = list(df['CLINIC_ZIP'])[i],
#                             clinic_type = list(df['CLINIC_TYPE'])[i],
#                             provider_name = list(df['PROVIDER_NAME'])[i],
#                             provider_type = list(df['PROVIDERTYPE__C'])[i],
#                             provider_category = list(df['PROVIDER_CATEGORY__C'])[i],
#                             client_naics = list(df['CLIENT_NAICS'])[i],
#                             client_id = list(df['CLIENT_ID'])[i],
#                             client_name = list(df['CLIENT NAME'])[i],
#                             parent_client_id = list(df['PARENT_CLIENT_ID'])[i],
#                             parent_client_name = list(df['PARENT CLIENT NAME'])[i],
#                             question_type = list(df['question_type'])[i],
#                             )
#         data.save()
#         print(i)
#     return HttpResponse('Hello')