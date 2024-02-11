from rest_framework import serializers
from agent.models import Business
from django.core.files.base import ContentFile
import base64
import binascii


class BusinessSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y | %H:%M:%S', required=False)
    image_base64 = serializers.CharField(required=False, allow_blank=True)
    department_display = serializers.SerializerMethodField(required=False)
    province_display = serializers.SerializerMethodField(required=False)
    district_display = serializers.SerializerMethodField(required=False)
    address_display = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Business
        fields = '__all__'

    def get_department_display(self, obj):
        if obj.department is not None:
            return obj.department.title
        return "Sin depa"

    def get_province_display(self, obj):
        if obj.province is not None:
            return obj.province.title
        return "Sin prov"

    def get_district_display(self, obj):
        if obj.district is not None:
            return obj.district.title
        return "Sin dist"
    def get_address_display(self, obj):
        if obj.address is not None:
            return obj.address
        return "Sin dirección"

    def validate_image_base64(self, value):
        if value is not None:
            try:
                base64.b64decode(value)
            except (TypeError, ValueError, binascii.Error):
                value = None
        return value

    def update(self, instance, validated_data):
        image_base64 = validated_data.pop('image_base64', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualizar la imagen si se proporciona una nueva base64
        if image_base64:
            image_data = base64.b64decode(image_base64)
            image_name = 'business/logo_{0}.png'.format(instance.id)
            instance.image.save(image_name, ContentFile(image_data))

        return instance