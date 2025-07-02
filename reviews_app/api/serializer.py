from rest_framework import serializers
from reviews_app.models import Review



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at', 'updated_at','reviewer',]

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)


    def validate(self, data):
        request = self.context['request']
        reviewer = request.user
        business_user = data.get('business_user')

        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError("Du hast diesen Benutzer bereits bewertet.")
        
        return data           