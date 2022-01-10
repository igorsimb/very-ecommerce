from rest_framework import serializers

from ecommerce.inventory.models import Product, ProductInventory, Brand, ProductAttributeValue, Media


class MediaImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ['image', 'alt_text']
        read_only = True

    def get_image(self, obj):
        return self.context['request'].build_absolute_uri()


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        exclude = ['id']
        depth = 2


class AllProducts(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ['name']  # exclude fields
        read_only = True
        editable = False


class ProductInventorySerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, read_only=True)
    attribute = ProductAttributeValueSerializer(source='attribute_values', many=True)  # we are hiding the real table
    # name ("attribute_values") and showing our made-up name ("attribute") to our api end-user
    image = MediaImageSerializer(source='media_product_inventory', many=True)

    class Meta:
        model = ProductInventory
        fields = [
            'sku',
            'image',
            'store_price',
            'is_default',
            'product',
            'product_type',
            'brand',
            'attribute',
        ]
        read_only = True
        # depth = 3  # How deep into table relationships (aka. foreign keys)
