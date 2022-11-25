from rest_framework import serializers
from .models import *


class CostSerializer(serializers.ModelSerializer):
	class Meta:
		model=CostModel
		fields=('total_cost','room','consumption',)

class ReadingSerializer(serializers.ModelSerializer):
	class Meta:
		model=ReadingModel
		fields=('consumption','datapoint','cost',)