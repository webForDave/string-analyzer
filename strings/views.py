from .models import String
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import StringSerializer
from .properties import return_string_properties, get_string_hashlib


@api_view(["POST"])
def get_string(request):
    serializer = StringSerializer(data=request.data)

    print(request.data)
    if serializer.is_valid():

        serializer.save(id=get_string_hashlib(request.data["value"]))
        response_data = serializer.data

        response_data["properties"] = return_string_properties(request.data["value"])

        return Response(response_data, status=status.HTTP_201_CREATED)
    else: 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)