from django.urls import path, include
from . import views

urlpatterns = [
    path('new', views.NewEnvironment.as_view(), name='new_environment'),
    path('all', views.ListEnvironments.as_view(), name='all_environments'),
    path('<int:environment_id>', views.DetailEnvironment.as_view(), name='environment'),
    path('update/<int:environment_id>', views.EnvironmentUpdate.as_view(), name='environment_update'),
    path('delete/<int:environment_id>', views.EnvironmentDelete.as_view(), name='environment_delete'),
    path('', views.EnvironmentsMenu.as_view(), name='environments_menu'),
]