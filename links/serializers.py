import re

from rest_framework import serializers

from .models import Link


domain_regex = re.compile(r"(\w){1,30}(\.)(\w){1,5}")


class PostLinkSerializer(serializers.ModelSerializer):
    links = serializers.ListField(
        child=serializers.CharField(), source="link", write_only=True)

    class Meta:
        model = Link
        fields = ("links",)

    def create(self, validated_data):
        links = validated_data.get("link")
        for link in links:
            domain = domain_regex.search(link)
            Link.objects.create(link=domain.group())
        return validated_data


class GetLinkSerializer(serializers.ModelSerializer):
    domains = serializers.CharField(source="link", read_only=True)

    class Meta:
        model = Link
        fields = ("domains",)
