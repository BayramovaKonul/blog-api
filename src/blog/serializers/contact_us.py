from rest_framework import serializers
from ..models import ContactUsModel

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields = ['email', 'subject', 'message']
