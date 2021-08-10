from rest_framework import serializers
# Create your serializers here.


class ExtraExpenseSerializer(serializers.Serializer):
    amount = serializers.CharField(max_length=100, null=True, blank=True)
    description = serializers.CharField(max_length=100, null=True, blank=True)
    date = serializers.DateField(blank=True, null=True)

    
