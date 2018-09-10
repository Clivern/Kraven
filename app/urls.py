"""
Routes For Kraven
"""

# Django
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

from app.controllers.web.admin.activity import Activity as Activity_View

from app.controllers.web.metric import Metric as Metric_View

from app.controllers.web.admin.hosts import Hosts_List as Hosts_List_Web
from app.controllers.web.admin.hosts import Host_Create as Host_Create_Web
from app.controllers.web.admin.hosts import Host_Edit as Host_Edit_Web
from app.controllers.web.admin.hosts import Host_View as Host_View_Web
from app.controllers.web.admin.hosts import Host_Containers_View as Host_Containers_View_Web

from app.controllers.web.admin.hosts import Host_Images_View as Host_Images_View_Web
from app.controllers.web.admin.hosts import Host_Images_Pull_View as Host_Images_Pull_View_Web
from app.controllers.web.admin.hosts import Host_Images_Build_View as Host_Images_Build_View_Web
from app.controllers.web.admin.hosts import Host_Networks_View as Host_Networks_View_Web
from app.controllers.web.admin.hosts import Host_Volumes_View as Host_Volumes_View_Web
from app.controllers.web.admin.hosts import Host_Actions_View as Host_Actions_View_Web
from app.controllers.web.admin.hosts import Host_Image_View as Host_Image_View_Web

from app.controllers.api.private.v1.install import Install as Install_V1_Endpoint_Private
from app.controllers.api.private.v1.login import Login as Login_V1_Endpoint_Private
from app.controllers.api.private.v1.register import Register as Register_V1_Endpoint_Private
from app.controllers.api.private.v1.forgot_password import Forgot_Password as Forgot_Password_V1_Endpoint_Private
from app.controllers.api.private.v1.reset_password import Reset_Password as Reset_Password_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.settings import Settings as Settings_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.profile import Profile as Profile_Admin_V1_Endpoint_Private

from app.controllers.api.private.v1.admin.hosts import Hosts as Hosts_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.hosts import Host as Host_Admin_V1_Endpoint_Private

from app.controllers.api.private.v1.admin.notifications import Notifications as Notifications_Admin_V1_Endpoint_Private

from app.controllers.api.private.v1.admin.actions.hosts import Health_Check as Health_Check_Action_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.actions.hosts import Pull_Image as Pull_Image_Action_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.actions.hosts import Build_Image as Build_Image_Action_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.actions.hosts import Get_Images as Get_Images_Action_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.actions.hosts import Search_Community_Images as Search_Community_Images_Action_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.actions.hosts import Prune_Unused_Images as Prune_Unused_Images_Action_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.actions.hosts import Prune_All_Unused_Images as Prune_All_Unused_Images_Action_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.actions.hosts import Remove_Image_By_Id as Remove_Image_By_Id_Action_Admin_V1_Endpoint_Private


urlpatterns = [
    # Public Views
    path('', Home_View.as_view(), name='app.web.home'),
    path('install', Install_View.as_view(), name='app.web.install'),
    path('login', Login_View.as_view(), name='app.web.login'),
    path('register', Register_View.as_view(), name='app.web.register'),
    path('forgot-password', Forgot_Password_View.as_view(), name='app.web.forgot_password'),
    path('reset-password/<token>', Reset_Password_View.as_view(), name='app.web.reset_password'),
    path('metrics/<type>', Metric_View.as_view(), name='app.web.metrics'),

    # Authenticated Users Views
    path('admin/', include([

        path('logout', Logout_View.as_view(), name='app.web.admin.logout'),
        path('dashboard', Dashboard_View.as_view(), name='app.web.admin.dashboard'),
        path('profile', Profile_View.as_view(), name='app.web.admin.profile'),

        path('hosts', Hosts_List_Web.as_view(), name='app.web.admin.hosts.list'),
        path('hosts/create', Host_Create_Web.as_view(), name='app.web.admin.hosts.create'),
        path('hosts/edit/<slug:host_slug>', Host_Edit_Web.as_view(), name='app.web.admin.hosts.edit'),
        path('hosts/view/<slug:host_slug>', Host_View_Web.as_view(), name='app.web.admin.hosts.view'),

        path('hosts/view/<slug:host_slug>/containers', Host_Containers_View_Web.as_view(), name='app.web.admin.hosts.view.containers'),

        path('hosts/view/<slug:host_slug>/images', Host_Images_View_Web.as_view(), name='app.web.admin.hosts.view.images'),
        path('hosts/view/<slug:host_slug>/images/pull', Host_Images_Pull_View_Web.as_view(), name='app.web.admin.hosts.view.pull.images'),
        path('hosts/view/<slug:host_slug>/images/build', Host_Images_Build_View_Web.as_view(), name='app.web.admin.hosts.view.build.images'),
        path('hosts/view/<slug:host_slug>/image/<image_id>', Host_Image_View_Web.as_view(), name='app.web.admin.hosts.view.image'),

        path('hosts/view/<slug:host_slug>/networks', Host_Networks_View_Web.as_view(), name='app.web.admin.hosts.view.networks'),
        path('hosts/view/<slug:host_slug>/volumes', Host_Volumes_View_Web.as_view(), name='app.web.admin.hosts.view.volumes'),
        path('hosts/view/<slug:host_slug>/actions', Host_Actions_View_Web.as_view(), name='app.web.admin.hosts.view.actions'),
        path('activity', Activity_View.as_view(), name='app.web.admin.activity.list'),
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
            path('notification', Notifications_Admin_V1_Endpoint_Private.as_view(), name='app.api.private.v1.admin.notifications.endpoint'),
            path('host', Hosts_Admin_V1_Endpoint_Private.as_view(), name='app.api.private.v1.admin.hosts.endpoint'),
            path('host/<int:host_id>', Host_Admin_V1_Endpoint_Private.as_view(), name='app.api.private.v1.admin.host.endpoint'),

            path(
                'action/host/health_check/<int:host_id>',
                Health_Check_Action_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.action.host.health_check.endpoint'
            ),
            path(
                'action/host/pull_image/<int:host_id>',
                Pull_Image_Action_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.action.host.pull_image.endpoint'
            ),
            path(
                'action/host/build_image/<int:host_id>',
                Build_Image_Action_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.action.host.build_image.endpoint'
            ),
            path(
                'action/host/get_images/<int:host_id>',
                Get_Images_Action_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.action.host.get_images.endpoint'
            ),
            path(
                'action/host/search_community_images/<int:host_id>',
                Search_Community_Images_Action_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.action.host.search_community_images.endpoint'
            ),
            path(
                'action/host/prune_unused_images/<int:host_id>',
                Prune_Unused_Images_Action_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.action.host.prune_unused_images.endpoint'
            ),
            path(
                'action/host/prune_all_unused_images/<int:host_id>',
                Prune_All_Unused_Images_Action_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.action.host.prune_all_unused_images.endpoint'
            ),
            path(
                'action/host/delete_image/<int:host_id>',
                Remove_Image_By_Id_Action_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.action.host.delete_image.endpoint'
            ),
        ]))

    ])),

    # Public API V1 Endpoints
    path('api/public/v1/', include([

    ]))
]

handler404 = handler404_view
handler500 = handler500_view
