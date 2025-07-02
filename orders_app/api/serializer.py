from rest_framework import serializers
from orders_app.models  import Order
from offers_app.models import OfferDetail


class ListCreateOrderSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions', 
            'delivery_time_in_days', 'price', 'features', 'offer_type',
            'status', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        offer_detail_id = validated_data.pop('offer_detail_id')
        offer_detail = OfferDetail.objects.select_related('offer').get(pk=offer_detail_id)

        order = Order.objects.create(
            customer_user=self.context['request'].user,
            business_user=offer_detail.offer.creator,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            **validated_data
        )
        return order
    
    def validate_offer_detail_id(self, value):
        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError('OfferDetail with this ID does not exist.')
        return value 
    



class SingleOrderSerializer(serializers.ModelSerializer):
    STATUS_CHOICES = ('in_progress', 'completed', 'cancelled')

    status = serializers.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions', 
            'delivery_time_in_days', 'price', 'features', 'offer_type',
            'created_at', 'updated_at'
        ]


    def validate_status(self,value):
        if value  not in self.STATUS_CHOICES:
             return serializers.ValidationError(f'Status nicht erlaubt! Erlaubt: {self.STATUS_CHOICES}')
        return value

       
   

