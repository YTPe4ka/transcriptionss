"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

def dashboard_view(request):
    """Renders visual frontend dashboard for exam presentation"""
    return render(request, 'index.html')

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),

    # REST API endpoints
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/categories/', include('apps.categories.urls')),
    path('api/v1/transactions/', include('apps.transactions.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),

    # Swagger / OpenAPI Schema endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
