from django.urls import path, include

urlpatterns = [
    path('github_projects/', include('github_projects.api.urls'))
]
