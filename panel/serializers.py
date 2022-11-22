from rest_framework import serializers
from .models import *


class CostSerializer(serializers.ModelSerializer):
	class Meta:
		model=CostModel
		fields=('month','total_cost','rating',)