from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from CustomAuth.views import user_registration, api_manager, views, manage_role

urlpatterns = [

    # start api urls
    path('api/userRegister/', views.userRegister, name='userRegister'),
    path('api/userLogin/', views.userLogin, name='userLogin'),
    path('api/patientRegister/', views.patientRegister, name='patientRegister'),
    # path('api/docUpload/', views.docUpload, name='docUpload'),
    # path('api_submit/', views.submit_patient, name='submit_patient'),
    path('api/userLogout/', views.userLogout, name='userLogout'),
    #  end api urls

    path("en/signup/", user_registration.multi_signup, name="account_signup"),
    path("signup/patient/", user_registration.signup_patient, name="signup_patient"),
    path("signup/staff/", user_registration.signup_staff, name="signup_staff"),

    path("check_login/<str:userid>/<str:password>/", api_manager.flutter_login, name="check_login"),
    path('userList/', api_manager.UserList.as_view({'get': 'list', 'post': 'create'}), name='userList'),
    path('userList/<int:pk>/', api_manager.UserList.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='userDetail'),

    path("profile/", TemplateView.as_view(template_name="dashboard.html"), name='profile'),
    path("user_profile/", TemplateView.as_view(template_name="account/profile.html"), name='user_profile'),

    path('Group/', manage_role.Group, name='Group'),
    path('submit_form/', manage_role.submit_form, name='submit_form'),
    path('delete_menu_item/', manage_role.delete_menu_item, name='delete_menu_item'),
    path('update-menu-item/', manage_role.update_menu_item, name='update_menu_item'),
    path('create_role/', manage_role.create_role, name='create_role'),
    path('get_role_menu_items/<int:role_id>/', manage_role.get_role_menu_items, name='get_role_menu_items'),
    path('edit_role/', manage_role.edit_role, name='edit_role'),
    # path('new_group/', manage_role.new_group, name='new_group'),
    path('delete_role/<int:role_id>/', manage_role.delete_role, name='delete_role'),
    path('create_group/', manage_role.create_group, name='create_group'),
    path('get_group_info/<int:group_id>/', manage_role.get_group_info, name='get_group_info'),
    path('edit_group/', manage_role.edit_group, name='edit_group'),
    path('delete_group/<int:group_id>/', manage_role.delete_group, name='delete_group'),
    path('create_user/', manage_role.create_user, name='create_user'),
    path('edit_user/', manage_role.edit_user, name='edit_user'),
    path('delete_user/', manage_role.delete_user, name='delete_user'),
    path('get_user_info/', manage_role.get_user_info, name='get_user_info'),
]
