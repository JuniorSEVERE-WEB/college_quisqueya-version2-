from rest_framework import serializers
from .models import Donation, EnrollmentFee

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = "__all__"

class EnrollmentFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentFee
        fields = "__all__"