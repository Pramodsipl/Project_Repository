from django.urls import path

from account_app.views import register_api, login_api ,get_data, update_user_data,partial_update,delete_user_data,reset_password,change_password,activate_account,logout_user

urlpatterns = [
    path('register_api/', register_api),

    path('login_api/', login_api),

    # path('get_data/<int:var>/', get_data, name='get_data'),
    path('get_data/', get_data, name='get_data'),

    # path('get_data/', get_data, name='get_data'),

    path('update_user_data/<int:update_id>/', update_user_data, name='update_user_data'),

    path('delete_user_data/<int:delete_id>/', delete_user_data),

    path('partial_update/<int:pathch_id>/',partial_update),

    path('reset_password/',reset_password),
    path('reset_password/<token>/',reset_password),
    path('change_password/',change_password),
    path('activate_account/<token>',activate_account),
    path("logout_user/",logout_user)

]