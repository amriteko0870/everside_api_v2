from unicodedata import name
from django.urls import path,include
from . import views


urlpatterns = [
    path('userLogin',views.userLogin,name='userLogin'),
    path('netPromoterScore',views.netPromoterScore,name='netPromoterScore'),
    path('netSentimentScore',views.netSentimentScore,name='netSentimentScore'),
    path('npsOverTime',views.npsOverTime,name='npsOverTime'),
    path('nssOverTime',views.nssOverTime,name='nssOverTime'),
    path('npsVsSentiments',views.npsVsSentiments,name='npsVsSentiments'),
    path('alertComments',views.alertComments,name='alertComments'),
    path('topComments',views.topComments,name='topComments'),
    path('totalComments',views.totalComments,name='totalComments'),
    path('clinicData',views.clinicData,name='clinicData'),
    path('totalCards',views.totalCards,name='totalCards'),
    path('egStatistics',views.egStatistics,name='egStatistics'),
    path('egPercentileMember',views.egPercentileMember,name='egPercentileMember'),
    path('filterRegion',views.filterRegion,name='filterRegion'),
    path('filterClinic',views.filterClinic,name='filterClinic'),

]
