import re
import redis

from datetime import datetime

from funbox.settings import REDIS_HOST, REDIS_PORT
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Link
from .serializers import PostLinkSerializer


domain_regex = re.compile(r"(\w){1,30}(\.)(\w){1,5}")

redis_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, db=1)
redis_test_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, db=2)


@api_view(["POST"])
def post_visited_links(request):
    db = redis_test_db if request.headers.get("Test") is not None else redis_db
    visit_date = str(int(datetime.now().timestamp()))
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

            db.sadd(visit_date, domain.group())
        db.rpush("list_of_keys", visit_date)
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)

    return Response(
        {"status": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
def get_visited_domains(request):
    db = redis_test_db if request.headers.get("Test") is not None else redis_db
    try:
        from_time = int(request.query_params.get("from"))
        to_time = int(request.query_params.get("to"))
        from_time is not None and to_time is not None
    except (ValueError, TypeError):
        return Response(
            {"status": "Параметры from и to должны быть числом."},
            status=status.HTTP_400_BAD_REQUEST
        )

    domains = set()
    for key in db.keys():
        if key != "list_of_keys":
            if (to_time >= int(key) >= from_time):
                domains = domains.union(db.smembers(key))
    domains = list(domains)
    return Response(
        {"domains": domains, "status": "ok"},
        status=status.HTTP_200_OK
    )
