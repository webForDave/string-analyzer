from .models import String
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import StringSerializer, SingleStringSerializer
from .properties import return_string_properties, get_string_hashlib
import datetime

@api_view(["GET", "DELETE"])
def get_or_delete_string(request, string_value):
    if request.method == "GET":
        try:
            string = String.objects.get(value=string_value)

            serializer = SingleStringSerializer(string)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except String.DoesNotExist:
            return Response({"error": "String does not exist in the system"}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == "DELETE":
        try:
            string = String.objects.get(value=string_value)
            string.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except String.DoesNotExist:
            return Response({"error": "String does not exist in the system"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
def strings_root(request):
    if request.method == "POST":
        serializer = StringSerializer(data=request.data)

        if not request.data or "value" not in request.data:
            return Response({"error": "Invalid request body or missing 'value' field"}, status=status.HTTP_400_BAD_REQUEST)

        if type(request.data["value"]) is not str:
            return Response({"error": "Invalid data type for 'value' (must be string)"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            string = String.objects.get(value=request.data["value"])

            if string:
                return Response({"error": "String already exists in the system"}, status=status.HTTP_409_CONFLICT)
            
        except String.DoesNotExist:

            if serializer.is_valid():

                id = get_string_hashlib(request.data["value"])
                properties = return_string_properties(request.data["value"])
                length = return_string_properties(request.data["value"])["length"]
                is_palindrome = return_string_properties(request.data["value"])["is_palindrome"]
                word_count = return_string_properties(request.data["value"])["word_count"]
                sha256_hash = return_string_properties(request.data["value"])["sha256_hash"]
                character_frequency_map = return_string_properties(request.data["value"])["character_frequency_map"]
                timestamp = datetime.datetime.utcnow().isoformat() + "Z"


                serializer.save(
                    id=id,
                    length=length, 
                    is_palindrome=is_palindrome,
                    word_count=word_count,
                    sha256_hash=sha256_hash,
                    character_frequency_map=character_frequency_map,
                    properties=properties,
                    created_at=timestamp
                )

                response_data = {"id": id, "value": request.data["value"], "properties": properties, "created_at": timestamp}

                return Response(response_data, status=status.HTTP_201_CREATED)