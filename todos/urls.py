from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('', views.TodosListView.as_view()),
    path('<int:pk>/', views.TodoDetailView.as_view()),
    path('create/', views.TodoCreateView.as_view()),
    path('update/<int:pk>/', views.TodoUpdateView.as_view()),
    path('delete/<int:pk>/', views.TodoDeleteView.as_view()),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]