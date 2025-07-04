
from rest_framework import serializers
from offers_app.models import Offer,OfferDetail
from django.contrib.auth.models import User

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = '__all__'
        read_only_fields = ['offer']

        
    def to_internal_value(self, data):
        data = data.copy()
        data['price'] = float(data.get('price', 0))
        data['delivery_time_in_days'] = int(data.get('delivery_time_in_days', 0))
        revisions = data.get('revisions', -1)
        data['revisions'] = int(revisions) if revisions != '' else -1
        return super().to_internal_value(data)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, required=False)
    user = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'description', 'image',
            'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
        read_only_fields = ['user', 'created_at','updated_at', 'min_price', 'min_delivery_time']

    def get_user(self, obj):
        return obj.creator.id

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        validated_data.pop('user', None)
        offer = Offer.objects.create(**validated_data)
        min_price=None
        min_delivery_time=None

        for detail_data in details_data:
            detail=OfferDetail.objects.create(offer=offer, **detail_data)
            
            if min_price is None or detail.price < min_price:
                min_price=detail.price
            if min_delivery_time is None or detail.delivery_time_in_days<min_delivery_time:
                min_delivery_time=detail.delivery_time_in_days

        if min_price is not None:
            offer.min_price = min_price 
        if min_delivery_time is not None:
            offer.min_delivery_time=min_delivery_time        
        offer.save()
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        validated_data.pop('user', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        image = validated_data.get('image', None)
        if image:
            instance.image = image
        instance.save()
        instance.details.all().delete()
        min_price = None
        min_delivery_time = None
    	
        for detail_data in details_data:
            detail = OfferDetail.objects.create(offer=instance, **detail_data)

            if min_price is None or detail.price < min_price:
                min_price = detail.price

            if min_delivery_time is None or detail.delivery_time_in_days < min_delivery_time:
                min_delivery_time = detail.delivery_time_in_days

        if min_price is not None:
            instance.min_price = min_price

        if min_delivery_time is not None:
            instance.min_delivery_time = min_delivery_time
        instance.save()
        return instance
           