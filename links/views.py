import re
import redis

from datetime import datetime

from funbox.settings import REDIS_HOST, REDIS_PORT
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Link
from .serializers import GetDomainSerializer, PostLinkSerializer


domain_regex = re.compile(r"(\w){1,30}(\.)(\w){1,5}")

redis_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@api_view(["POST"])
def post_visited_links(request):
    visit_date = int(datetime.now().timestamp())
    serializer = PostLinkSerializer(data=request.data)
    if serializer.is_valid():
        links = serializer.validated_data.get("link")
        for link in links:
            domain = domain_regex.search(link)
            if domain is None:
                return Response(
                    {"status": f"Неправильный формат ссылки: {link}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            Link.objects.create(visit_date=visit_date, link=domain.group())
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)

    return Response(
        {"status": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
def get_visited_domains(request):
    print(request.query_params)
    try:
        from_time = int(request.query_params.get("from"))
        to_time = int(request.query_params.get("to"))
    except ValueError:

        return Response(
            {"status": "Параметры from и to должны быть числом."},
            status=status.HTTP_400_BAD_REQUEST
        )
    if from_time is not None and to_time is not None:
        domains = Link.objects.order_by().filter(
            visit_date__gte=from_time, visit_date__lte=to_time
        ).values("link").distinct()
    else:
        domains = Link.objects.order_by().values("link").distinct()
    serializer = GetDomainSerializer(domains, many=True)
    values = [dct["domains"] for dct in serializer.data]
    return Response(
        {"domains": values, "status": "ok"},
        status=status.HTTP_200_OK
    )
