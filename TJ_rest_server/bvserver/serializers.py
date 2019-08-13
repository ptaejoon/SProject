from rest_framework import serializers
from . import models

class productCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductCategories
        fields = '__all__'

class productCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Companies
        fields = '__all__'

class productImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductImages
        fields = '__all__'

class productSerializer(serializers.ModelSerializer):
    category = productCategorySerializer()
    company = productCompanySerializer()
    class Meta:
        model = models.Products
        fields = '__all__'

class materialSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Materials
        fields = '__all__'

class productMaterialSerializer(serializers.ModelSerializer):

    product = productSerializer()
    material = materialSerializer()
    class Meta:
        model = models.ProductMaterial
        fields = '__all__'


class productSpecSerializer(serializers.ModelSerializer):
    product = productSerializer()

    class Meta:
        model = models.ProductImages
        fields = '__all__'
