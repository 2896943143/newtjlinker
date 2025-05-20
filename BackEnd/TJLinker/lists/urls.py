from django.urls import path, include
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ActivitySearchSet
from .views import GetClassView, GetActBasicAllView, GetActBasicByClassView, SearchActivityView
from .views import GetActivityDetailView
from .views import GetActivitiesByCategoryView
from .views import SendMessageGroup, GetLatestMessagesView
from .views import JoinActivityView
from .views import GetActivityStateView
from .views import GetChatMessagesView, SendMessageView
from .views import SearchAndFilterActivitiesView
from .views import NewGetChatList
from .views import DeleteTeamView
from .views import SearchAndFilterDingYueActivitiesView
from .views import BreakeActivityView
from  .views import GetActivityParticipantView
from .views import SendPersonalMessageView
from .views import GetPersonalChatMessagesView
from .views import GetLatestPersonalMessagesView
from .views import GetLastMessagesView
from .views import LoadMessagePerson
from .views import SendMessageViewPerson
from .views import LoadMessageGroup

router = DefaultRouter()
router.register(r'create_activities', ActivityViewSet, basename='activity')
router.register(r'search_activities', ActivitySearchSet, basename='activity_search')

urlpatterns = [
    path('', include(router.urls)),
    path('get_class/', GetClassView.as_view(), name='get_class'),
    path('get_actbasic_all/', GetActBasicAllView.as_view(), name='get_actbasic_all'),
    path('get_actbasic_byclass/<str:classID>/', GetActBasicByClassView.as_view(), name='get_actbasic_byclass'),
    path('search_activity/<str:word>/', SearchActivityView.as_view(), name='search_activity'),
    path('get_activity_detail/<str:activityID>/', GetActivityDetailView.as_view(), name='get_activity_detail'),
    path('get_activities_by_category/', GetActivitiesByCategoryView.as_view(), name='get_activities_by_category'),
    path('join_activity/', JoinActivityView.as_view(), name='join_activitie'),
    path('get_activity_state/', GetActivityStateView.as_view(), name='get_activitity_state'),
    path('get_chat_messages/', GetChatMessagesView.as_view(), name='get_chat_messages'),
    path('send_message/', SendMessageView.as_view(), name='send_message'),
    path('search_and_filter_activities/', SearchAndFilterActivitiesView.as_view(), name='search_and_filter_activities'),
    path('search_and_filter_dingyueactivities/', SearchAndFilterDingYueActivitiesView.as_view(), name='search_and_filter_dingyueactivities'),
    path('DeleteTeam/', DeleteTeamView.as_view(), name='delete-team'),
    path('break_activity/', BreakeActivityView.as_view(), name='breake_activity'),
    path('activity_members/', GetActivityParticipantView.as_view(), name='activity_members'),
    path('send_message_personal/', SendPersonalMessageView.as_view(), name='send_message_personal'),
    path('get_chat_messages_personal/', GetPersonalChatMessagesView.as_view(), name='get_chat_messages_personal'),
    path('get_latest_messages_personal/', GetLatestPersonalMessagesView.as_view(), name='get_latest_messages_personal'),
    path('get_last_messages/', GetLastMessagesView.as_view(), name='get_last_messages'),
    path('get_chat_messages/', GetChatMessagesView.as_view(), name='get_chat_messages'),
    path('get_latest_messages/', GetLatestMessagesView.as_view(), name='get_latest_messages'),

    path('new_get_chat_list/',NewGetChatList.as_view(),name='new_get_chat_list'),
    path('load_message_person/',LoadMessagePerson.as_view(),name='load_message_person'),
    path('load_message_group/',LoadMessageGroup.as_view(),name='load_message_group'),
    path('send_message_person/', SendMessageViewPerson.as_view(), name='send_message_person'),
    path('send_message_group/',SendMessageGroup.as_view(),name='send_message_group'),
]
