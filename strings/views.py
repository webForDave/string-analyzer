from .models import String
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import StringSerializer, SingleStringSerializer
from .properties import return_string_properties, get_string_hashlib
from .filters import AnalyzedStringFilter
from .utils import parse_natural_language_query
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

    if request.method == "GET":
        queryset = String.objects.all()

        filterset = AnalyzedStringFilter(request.query_params, queryset=queryset)
        
        if not filterset.is_valid():
            return Response(
                {"detail": filterset.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        final_queryset = filterset.qs
        
        serializer = StringSerializer(final_queryset, many=True)
        
        filters_applied = {}
        valid_filters = filterset.filters.keys()

        for key, value in request.query_params.items():
            if key in valid_filters: 
                filters_applied[key] = value

        return Response({
            "data": serializer.data,
            "count": final_queryset.count(),
            "filters_applied": filters_applied
        }, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def natural_language_filter_view(request):
    query = request.query_params.get('query')
    if not query:
        return Response(
            {"detail": "Missing 'query' parameter."},
            status=status.HTTP_400_BAD_REQUEST
        )

    original_query = query
    
    try:
        parsed_filters = parse_natural_language_query(query)
        
        queryset = String.objects.all()
        filterset = AnalyzedStringFilter(parsed_filters, queryset=queryset)
        
        if not filterset.is_valid():
            raise ValueError(f"Query parsed but resulted in conflicting or invalid filter values: {filterset.errors}")

        final_queryset = filterset.qs
        
    except ValueError as e:
        error_message = str(e)
        if "Conflicting" in error_message:
            return Response(
                {"detail": error_message},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        else:
            return Response(
                {"detail": error_message}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {"detail": f"An unexpected server error occurred: {e}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
    serializer = SingleStringSerializer(final_queryset, many=True)

    return Response({
        "data": serializer.data,
        "count": final_queryset.count(),
        "interpreted_query": {
            "original": original_query,
            "parsed_filters": parsed_filters
        }
    }, status=status.HTTP_200_OK)