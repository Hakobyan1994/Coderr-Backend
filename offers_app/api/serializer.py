
from rest_framework import serializers
from offers_app.models import Offer,OfferDetail
from django.contrib.auth.models import User
from collections import OrderedDict 




class OfferDetailMiniSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ("id", "url")    
        extra_kwargs = {
            "url": {
                "view_name": "offer-detail-single",   
                "lookup_field": "pk",
            }
        }


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'offer_type',
            'price',
            'delivery_time_in_days',
            'revisions',
            'features'
        ]

        
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
        fields = ['username', 'first_name', 'last_name']

class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, write_only=True, required=False)
    details_mini = OfferDetailMiniSerializer(source="details", many=True, read_only=True)
    user = serializers.SerializerMethodField()
    user_details = UserSerializer(source="creator", read_only=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'description', 'image',
            'created_at', 'updated_at','details', "user_details",'details_mini', 'min_price', 'min_delivery_time',]
        read_only_fields = ['user',"user_details", 'created_at','updated_at', 'min_price', 'min_delivery_time']

    def get_user(self, obj):
        return obj.creator.id


    def _ordered_output(self,rep, details_data):
        order = ["id", "user", "title", "description", "image", "created_at", "updated_at", "details","min_price", "min_delivery_time", "user_details",]
        out = OrderedDict()
        for key in order:
            if key == "details":
                out[key] = details_data
            elif key in rep:
                out[key] = rep[key]
        return out



    def to_representation(self, instance):
        rep     = super().to_representation(instance)
        if self.context.get("is_detail"):
         rep.pop("user_details", None)
        request = self.context.get("request")
        if request and request.method == "POST":
            rep["details"] = OfferDetailSerializer(instance.details.all(), many=True).data
            rep.pop("details_mini", None)
            rep.pop("min_price",   None)
            rep.pop("min_delivery_time", None)
            rep.pop("user_details",None)
            return rep
        details_data = rep.pop("details_mini", [])
        return self._ordered_output(rep, details_data)


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