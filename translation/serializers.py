from abc import ABC

from rest_framework import serializers
from .models import Endpoint, EnglishToHindiTranslation, MLAlgorithm, MLRequest


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ('id', 'name', 'owner', 'created_at')
        fields = read_only_fields


class MLAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithm
        read_only_fields = ('name','description','code','version','owner','created_at','parent_endpoint')
        fields = read_only_fields


class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = ('id','input_data','full_response','response','created_at','parent_mlalgorithm')
        fields = ('id','input_data','full_response','response','created_at','parent_mlalgorithm','feedback')



class PersonDataSerialzer(serializers.Serializer):
    full_name = serializers.CharField(max_length=1024,allow_blank=True,required=False)
    full_address = serializers.CharField(max_length=2048,allow_blank=True,allow_null=True,required=False)
    relation_name = serializers.CharField(max_length=1024, allow_blank=True,allow_null=True,required=False)



