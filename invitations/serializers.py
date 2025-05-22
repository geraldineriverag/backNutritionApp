# invitations/serializers.py

import uuid
from rest_framework import serializers
from .models import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    nutritionist           = serializers.PrimaryKeyRelatedField(read_only=True)
    token                  = serializers.CharField(read_only=True)
    accepted               = serializers.BooleanField(read_only=True)
    accepted_at            = serializers.DateTimeField(read_only=True)
    nutritionist_name      = serializers.CharField(source='nutritionist.user.first_name', read_only=True)
    nutritionist_email     = serializers.EmailField(source='nutritionist.user.email',   read_only=True)

    class Meta:
        model = Invitation
        fields = [
            'id',
            'nutritionist',
            'email',
            'token',
            'created_at',
            'accepted',
            'accepted_at',
            'nutritionist_name',
            'nutritionist_email',
        ]
        read_only_fields = [
            'id',
            'nutritionist',
            'token',
            'created_at',
            'accepted',
            'accepted_at',
            'nutritionist_name',
            'nutritionist_email',
        ]

    def create(self, validated_data):
        # 1) Le ponemos el nutritionist del request
        validated_data['nutritionist'] = self.context['request'].user.nutritionist_profile
        # 2) Generamos un token único
        validated_data['token'] = uuid.uuid4().hex
        return super().create(validated_data)
