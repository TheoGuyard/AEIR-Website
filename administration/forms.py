from adhesion.models import Adhesion
from django_filters import FilterSet

class AdhesionFilter(FilterSet):
    class Meta:
        model = Adhesion
        fields = {
            'first_name': ['exact'],
            'last_name': ['exact'],
            'school_year': ['exact'],
            'departement' : ['exact'],
            'id': ['exact'],
        }