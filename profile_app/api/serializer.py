from rest_framework import serializers
from profile_app.models import BusinessProfile,CustomerProfile


class BusinessProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', default='', allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', default='', allow_blank=True)
    username = serializers.CharField(source='user.username', read_only=True)
    created_at = serializers.DateTimeField(source='user.date_joined', read_only=True)
    email = serializers.EmailField(source='user.email', default='', allow_blank=True)
    user = serializers.IntegerField(source='user.id', read_only=True)
    type = serializers.CharField(source='user_type', read_only=True)
    file = serializers.FileField(required=False, allow_null=True)
        
    class Meta:
        model = BusinessProfile
        fields = [
            'user', 'first_name', 'username', 'last_name', 'email', 'created_at',
            'file', 'tel', 'location', 'description', 'working_hours', 'type'
        ]
            

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return super().update(instance, validated_data)


class CustomerProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', default='', allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', default='', allow_blank=True)
    username = serializers.CharField(source='user.username', read_only=True)
    created_at = serializers.DateTimeField(source='user.date_joined', read_only=True)
    email = serializers.EmailField(source='user.email', default='', allow_blank=True)
    user = serializers.IntegerField(source='user.id', read_only=True)
    type = serializers.CharField(source='user_type', read_only=True)
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = CustomerProfile
        fields = [
            'user', 'first_name', 'username', 'last_name', 'email', 'created_at',
            'file', 'type'
        ]
                            
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return super().update(instance, validated_data)        
           







