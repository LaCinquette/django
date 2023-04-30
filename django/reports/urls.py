from django.urls import path, include
from . import views

urlpatterns = [
    path('new', views.ReportCreate.as_view(), name='new_report'),
    path('all', views.ReportList.as_view(), name='all_reports'),
    path('<int:report_id>', views.ReportDetail.as_view(), name='report'),
    path('update/<int:report_id>', views.ReportUpdate.as_view(), name='report_update'),
    path('delete/<int:report_id>', views.ReportDelete.as_view(), name='report_delete'),
    path('search', views.SearchView.as_view(), name='search'),
    path('search/results', views.SearchResultsList.as_view(), name='results'),
    path('', views.ReportsMenu.as_view(), name='reports_menu'),
]