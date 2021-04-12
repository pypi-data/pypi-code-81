from django.urls import path

from medicine.views import query_medicine, match_medicine, query_trend

urlpatterns = [
    path('', query_medicine),
    path('trend', query_trend),
    path('match', match_medicine)
]
