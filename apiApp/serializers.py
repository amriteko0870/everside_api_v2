from rest_framework import serializers
from apiApp.models import *

class everside_nps_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = everside_nps
        fields = [
                    'review_ID',
                    'review',
                    'label',
                    'polarity_score',
                    'nps_score',
                    'nps_label',
                    'date',
                    'clinic',
                    'city',
                    'state',
                    'timestamp',
                ]

class eversideAlertComments(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = everside_nps
        fields = [
                'id',
                'review',
                'label',
                'date'
                ]

class eversideComments(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = everside_nps
        fields = [
                'id',
                'review',
                'label',
                ]