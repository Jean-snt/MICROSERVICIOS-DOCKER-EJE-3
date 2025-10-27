from rest_framework import serializers


class LoanCreationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    book_id = serializers.IntegerField()


class LoanResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    loan_date = serializers.DateField()
    due_date = serializers.DateField()
    status = serializers.CharField()