from django.urls import path
from .views import SummaryReportView, CategoryBreakdownReportView

urlpatterns = [
    path('summary/', SummaryReportView.as_view(), name='report_summary'),
    path('by-category/', CategoryBreakdownReportView.as_view(), name='report_by_category'),
]
