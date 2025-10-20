from .models import String
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import StringSerializer, SingleStringSerializer
from .properties import return_string_properties, get_string_hashlib

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
    if request.method == "GET":
        strings_qs = String.objects.all()
        filters_applied = {}

        is_palindrome = request.query_params.get("is_palindrome")
        min_length = request.query_params.get("min_length")
        max_length = request.query_params.get("max_length")
        word_count = request.query_params.get("word_count")
        contains_character = request.query_params.get("contains_character")

        if is_palindrome is not None:
            val = is_palindrome.lower()
            if val not in ("true", "false"):
                return Response(
                    {"error": "is_palindrome must be 'true' or 'false'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            bool_val = val == "true"
            strings_qs = strings_qs.filter(is_palindrome=bool_val)
            filters_applied["is_palindrome"] = bool_val

        if min_length:
            if not min_length.isdigit():
                return Response({"error": "min_length must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
            strings_qs = strings_qs.filter(length__gte=int(min_length))
            filters_applied["min_length"] = int(min_length)

        if max_length:
            if not max_length.isdigit():
                return Response({"error": "max_length must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
            strings_qs = strings_qs.filter(length__lte=int(max_length))
            filters_applied["max_length"] = int(max_length)

        if word_count:
            if not word_count.isdigit():
                return Response({"error": "word_count must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
            strings_qs = strings_qs.filter(word_count=int(word_count))
            filters_applied["word_count"] = int(word_count)

        if contains_character:
            if len(contains_character) != 1:
                return Response({"error": "contains_character must be a single character."}, status=status.HTTP_400_BAD_REQUEST)
            strings_qs = strings_qs.filter(value__icontains=contains_character)
            filters_applied["contains_character"] = contains_character

        serializer = SingleStringSerializer(strings_qs, many=True)

        return Response(
            {
                "data": serializer.data,
                "count": strings_qs.count(),
                "filters_applied": filters_applied,
            },
            status=status.HTTP_200_OK,
        )
    
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

                serializer.save(
                    id=id,
                    length=length, 
                    is_palindrome=is_palindrome,
                    word_count=word_count,
                    sha256_hash=sha256_hash,
                    character_frequency_map=character_frequency_map,
                    properties=properties
                )

                response_data = {"id": id, "value": request.data["value"], "properties": properties}

                return Response(response_data, status=status.HTTP_201_CREATED)