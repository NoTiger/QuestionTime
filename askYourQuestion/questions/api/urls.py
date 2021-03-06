from django.urls import include, path
from rest_framework.routers import DefaultRouter

from questions.api import views

router = DefaultRouter()
router.register(r"questions", views.QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('questions/<slug:slug>/answers/', views.AnswerListAPIView.as_view(), name='answer-list'),
    path('questions/<slug:slug>/answer/',
         views.AnswerCreateAPIView.as_view(),
         name='answer-create'),
    path('answers/<int:pk>/',
         views.AnswerRUDAPIView.as_view(),
         name='answer-detail'),
    path('answers/<int:pk>/like/',
         views.AnswerLikeAPIView.as_view(),
         name='answer-like'),
]
