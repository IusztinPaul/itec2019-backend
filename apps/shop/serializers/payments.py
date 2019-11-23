from typing import List

from django.db import transaction
from django.db.models import Model
from rest_framework import serializers

from apps.common.utils import get_or_create_model
from apps.shop import models
from apps.shop.serializers import ProductSerializer


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shipment
        fields = ("status", "provider")


class PaymentProductSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=models.Product.objects.all(),
        source='product'
    )

    product = ProductSerializer(read_only=True)

    class Meta:
        model = models.PaymentProduct
        fields = ("counter", "product", "product_id")


class PaymentSerializer(serializers.Serializer):
    optional = serializers.CharField(required=False)
    status = serializers.CharField(read_only=True)

    products = PaymentProductSerializer(many=True)

    class Meta:
        model = models.Payment
        fields = ("status", "optional", "products")
        read_only_fields = ("id", "status")

    def create(self, validated_data):
        products = validated_data.pop('products')

        with transaction.atomic():

            payment = models.Payment(**validated_data)
            payment.save()

            self._get_or_create_products(payment, products)

        return payment

    def _get_or_create_products(self, payment: Model, products: List[dict]):
        for payment_product in products:
            payment_product['product_id'] = payment_product['product'].id
            get_or_create_model(
                payment_product,
                PaymentProductSerializer,
                payment=payment,
            )
