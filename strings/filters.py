import django_filters
from .models import String

class AnalyzedStringFilter(django_filters.FilterSet):
    is_palindrome = django_filters.BooleanFilter(field_name='is_palindrome')

    min_length = django_filters.NumberFilter(field_name='length', lookup_expr='gte')

    max_length = django_filters.NumberFilter(field_name='length', lookup_expr='lte')

    word_count = django_filters.NumberFilter(field_name='word_count', lookup_expr='exact')
    
    contains_character = django_filters.CharFilter(method='filter_contains_character')

    class Meta:
        model = String
        fields = ['is_palindrome', 'min_length', 'max_length', 'word_count', 'contains_character']

    def filter_contains_character(self, queryset, name, value):
        return queryset.filter(value__icontains=value)