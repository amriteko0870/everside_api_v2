from datetime import datetime
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
                'clinic',
                'timestamp'
                ]
    def to_representation(self, data):
        data = super(eversideAlertComments, self).to_representation(data)
        data['timestamp'] = dt_object = datetime.fromtimestamp(data.get('timestamp')).strftime('%b,%Y')
        return data

class eversideComments(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = everside_nps
        fields = [
                'id',
                'review',
                'label',
                'timestamp',
                ]
    def to_representation(self, data):
        data = super(eversideComments, self).to_representation(data)
        data['timestamp'] = dt_object = datetime.fromtimestamp(data.get('timestamp')).strftime('%b,%Y')
        return data

class eversideProviders(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = everside_nps
        fields = [
            'provider_name',
            'provider_type',
            'provider_category',
            ]
class eversideClient(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = everside_nps
        fields = [
            "client_name",
            "parent_client_name"
            ]