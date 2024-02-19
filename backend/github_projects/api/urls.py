from rest_framework.routers import SimpleRouter

from github_projects.api import views

app_name = "github_projects"

router = SimpleRouter()
router.register("", views.GithubViewSet, basename="github")

urlpatterns = [
    *router.urls,
]
