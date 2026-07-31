from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'name_uz', 'name_ru', 'name_en', 'type', 'icon', 'color', 'user')
        read_only_fields = ('id', 'user')

    def get_name(self, obj):
        request = self.context.get('request')
        lang = 'uz'
        if request:
            # Query param takes precedence, then Accept-Language header
            lang = request.query_params.get('lang') or request.META.get('HTTP_ACCEPT_LANGUAGE', 'uz')
            lang = lang[:2].lower()
        return obj.get_name(lang)

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
