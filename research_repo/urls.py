from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import LoginView, PublicationListView, PublicationDetailView, LogoutView, SignUpView, PublicationCreateView, PublicationUpdateView, PublicationDeleteView, UploadDocumentView,AccessGrantCreateView, SettingsView

urlpatterns = [
    path('', views.DiscoveryView.as_view(), name='discovery'),
    path('register/', views.SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('publication-list', PublicationListView.as_view(), name='publication_list'),
    path('publications/<int:pk>/', PublicationDetailView.as_view(), name='publication_detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('publications/create/', PublicationCreateView.as_view(), name='publication_create'),
    path('publications/<int:pk>/update/', PublicationUpdateView.as_view(), name='publication_update'),
    path('publications/<int:pk>/delete/', PublicationDeleteView.as_view(), name='publication_delete'),
    path('upload-document/', UploadDocumentView.as_view(), name='upload_document'),
    path('access-grant/',AccessGrantCreateView.as_view(), name = 'grant_access'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]