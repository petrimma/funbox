from rest_framework import serializers

from .models import Link


class GetDomainSerializer(serializers.ModelSerializer):
    domains = serializers.CharField(source="link", read_only=True)

    class Meta:
        model = Link
        fields = ("domains",)


class PostLinkSerializer(serializers.ModelSerializer):
    links = serializers.ListField(
        child=serializers.CharField(), source="link", write_only=True)

    class Meta:
        model = Link
        fields = ("links",)

    def validate(self, data):
        links = data.get("link")
        if links == []:
            raise serializers.ValidationError("В запросе нет ни одной ссылки.")
        return data
