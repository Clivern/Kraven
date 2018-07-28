"""
Routes For Kraven
"""

# Django
from django.contrib import admin
from django.urls import include, path

# local Django
from app.controllers.web.home import Home as Home_View
from app.controllers.web.install import Install as Install_View
from app.controllers.web.not_found import handler404 as handler404_view
from app.controllers.web.error import handler500 as handler500_view
from app.controllers.web.login import Login as Login_View
from app.controllers.web.register import Register as Register_View
from app.controllers.web.forgot_password import Forgot_Password as Forgot_Password_View
from app.controllers.web.reset_password import Reset_Password as Reset_Password_View

from app.controllers.web.admin.logout import Logout as Logout_View
from app.controllers.web.admin.dashboard import Dashboard as Dashboard_View
from app.controllers.web.admin.profile import Profile as Profile_View

from app.controllers.web.admin.settings import Settings as Settings_View


from app.controllers.web.admin.hosts import Hosts_List as Hosts_List_Web
from app.controllers.web.admin.hosts import Host_Create as Host_Create_Web
from app.controllers.web.admin.hosts import Host_Edit as Host_Edit_Web
from app.controllers.web.admin.hosts import Host_View as Host_View_Web


from app.controllers.api.private.v1.install import Install as Install_V1_Endpoint_Private
from app.controllers.api.private.v1.login import Login as Login_V1_Endpoint_Private
from app.controllers.api.private.v1.register import Register as Register_V1_Endpoint_Private
from app.controllers.api.private.v1.forgot_password import Forgot_Password as Forgot_Password_V1_Endpoint_Private
from app.controllers.api.private.v1.reset_password import Reset_Password as Reset_Password_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.settings import Settings as Settings_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.profile import Profile as Profile_Admin_V1_Endpoint_Private

from app.controllers.api.private.v1.admin.hosts import Hosts as Hosts_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.hosts import Host as Host_Admin_V1_Endpoint_Private



urlpatterns = [
    # Public Views
    path('', Home_View.as_view(), name='app.web.home'),
    path('install', Install_View.as_view(), name='app.web.install'),
    path('login', Login_View.as_view(), name='app.web.login'),
    path('register', Register_View.as_view(), name='app.web.register'),
    path('forgot-password', Forgot_Password_View.as_view(), name='app.web.forgot_password'),
    path('reset-password/<token>', Reset_Password_View.as_view(), name='app.web.reset_password'),

    # Authenticated Users Views
    path('admin/', include([

        path('logout', Logout_View.as_view(), name='app.web.admin.logout'),
        path('dashboard', Dashboard_View.as_view(), name='app.web.admin.dashboard'),
        path('profile', Profile_View.as_view(), name='app.web.admin.profile'),


        path('hosts', Hosts_List_Web.as_view(), name='app.web.admin.hosts.list'),
        path('hosts/create', Host_Create_Web.as_view(), name='app.web.admin.hosts.create'),
        path('hosts/edit/<slug:host_slug>', Host_Edit_Web.as_view(), name='app.web.admin.hosts.edit'),
        path('hosts/view/<slug:host_slug>', Host_View_Web.as_view(), name='app.web.admin.hosts.view'),



        path('settings', Settings_View.as_view(), name='app.web.admin.settings'),

    ])),

    # Private API V1 Endpoints
    path('api/private/v1/', include([

        path('install', Install_V1_Endpoint_Private.as_view(), name='app.api.private.v1.install.endpoint'),
        path('login', Login_V1_Endpoint_Private.as_view(), name='app.api.private.v1.login.endpoint'),
        path('register', Register_V1_Endpoint_Private.as_view(), name='app.api.private.v1.register.endpoint'),
        path('forgot-password', Forgot_Password_V1_Endpoint_Private.as_view(), name='app.api.private.v1.forgot_password.endpoint'),
        path('reset-password', Reset_Password_V1_Endpoint_Private.as_view(), name='app.api.private.v1.reset_password.endpoint'),

        path('admin/', include([
            path('settings', Settings_Admin_V1_Endpoint_Private.as_view(), name='app.api.private.v1.admin.settings.endpoint'),
            path('profile', Profile_Admin_V1_Endpoint_Private.as_view(), name='app.api.private.v1.admin.profile.endpoint'),

            path('host', Hosts_Admin_V1_Endpoint_Private.as_view(), name='app.api.private.v1.admin.hosts.endpoint'),
            path('host/<int:host_id>', Host_Admin_V1_Endpoint_Private.as_view(), name='app.api.private.v1.admin.host.endpoint'),

        ]))

    ])),

    # Public API V1 Endpoints
    path('api/public/v1/', include([

    ]))
]

handler404 = handler404_view
handler500 = handler500_view