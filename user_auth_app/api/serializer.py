from rest_framework import serializers
from user_auth_app.models import Profile
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profile_app.models import BusinessProfile,CustomerProfile

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True, required=True)
    type = serializers.ChoiceField(choices=Profile.PROFILE_TYPES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': ['Passwörter stimmen nicht überein.']})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': ['Diese E-Mail wird bereits verwendet.']})
        return data
        
    def create(self, validated_data):
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user, user_type=user_type)
        if user_type == 'business':
            BusinessProfile.objects.create(
                user=user,
                user_type='business',
                username=user.username,
                email=user.email,
                first_name='',
                last_name='',
                tel='',
                location='',
                description='',
                working_hours='',
                created_at='',
                file=None
            )
        else:
            CustomerProfile.objects.create(
                user=user,
                user_type='customer',
                username=user.username,
                email=user.email,
                first_name='',
                last_name='',
                created_at='',
                file=None
            )
        return user
    