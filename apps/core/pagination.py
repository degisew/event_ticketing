from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class Pagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "results": data,
                "metadata": {
                    "limit": self.limit,
                    "offset": self.offset,
                    "total": self.count,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
            }
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "results": schema,
                "metadata": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer"},
                        "offset": {"type": "integer"},
                        "total": {"type": "integer"},
                        "next": {"type": "string", "format": "uri"},
                        "previous": {"type": "string", "format": "uri"},
                    },
                },
            },
        }
