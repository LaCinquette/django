from django.urls import path, include
from . import views

urlpatterns = [
    path('new', views.NewSoftware.as_view(), name='new_software'),
    path('all', views.ListSoftware.as_view(), name='all_software'),
    path('<int:software_id>', views.DetailSoftware.as_view(), name='software'),
    path('update/<int:software_id>', views.SoftwareUpdate.as_view(), name='software_update'),
    path('delete/<int:software_id>', views.SoftwareDelete.as_view(), name='software_delete'),
    path('', views.SoftwareMenu.as_view(), name='software_menu'),
]