from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class CreateLoanSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    book_id = serializers.IntegerField()