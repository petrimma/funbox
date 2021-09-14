from datetime import datetime

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Link
from .serializers import GetLinkSerializer, PostLinkSerializer


class LinkViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == "list":
            return GetLinkSerializer
        else:
            return PostLinkSerializer

    def list(self, request):
        response = super(LinkViewSet, self).list(request)
        values = [list(dict.values())[0] for dict in response.data]
        status = "ok" if response.status_code == 200 else str(
            response.status_code)

        response.data = {"domains": values, "status": status}

        return response

    def get_queryset(self):
        params = self.request.query_params
        time_from_unix = params.get("from")
        time_to_unix = params.get("to")
        if time_from_unix is not None and time_to_unix is not None:
            time_from_dt = datetime.utcfromtimestamp(int(time_from_unix))
            time_to_dt = datetime.utcfromtimestamp(int(time_to_unix))
            queryset = Link.objects.order_by().filter(
                visit_date__gt=time_from_dt, visit_date__lt=time_to_dt
            ).values("link").distinct()
        else:
            queryset = Link.objects.order_by().values("link").distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"status": "ok"}, status=status.HTTP_201_CREATED, headers=headers
        )
