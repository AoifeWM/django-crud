from django.urls import path
from .views import SnackListView, SnackCreateView, SnackDeleteView, SnackDetailView, SnackUpdateView


urlpatterns = [
    path('', SnackListView.as_view(), name='snack_list'),
    path('<int:pk>/', SnackDetailView.as_view(), name='snack_detail'),
    path('<int:pk>/update/', SnackUpdateView.as_view(), name='snack_update'),
    path('<int:pk>/delete/', SnackDeleteView.as_view(), name='snack_delete'),
    path('create/', SnackCreateView.as_view(), name='snack_create'),
]
