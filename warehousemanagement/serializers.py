from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'pk',
            'url',
            'manufacturer_name',
            'model_name',
            'price',
            'quantity',
        ]
        read_only_fields = ['pk', 'url', 'quantity']

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)
