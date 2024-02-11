from rest_framework import serializers
from django.core.files.base import ContentFile
import base64
import six
import uuid
from users.models import User

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = f"{file_name}.{file_extension}"
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension

class UserSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(
        max_length=None, use_url=True, required=False, allow_null=True
    )
    password = serializers.CharField(write_only=True, required=True)
    role_display = serializers.SerializerMethodField(required=False)


    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'photo', 'document_type', 'document_number', 'phone_code', 'phone_number', 'role', 'password', 'role_display')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'photo' and value is None:
                continue
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def get_role_display(self, obj):
        return obj.get_role_str()