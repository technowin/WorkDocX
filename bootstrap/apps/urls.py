from django.urls import path

from .views import (
    # calendar
    EventListView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    apps_calendar_calendar_view,

    #Chat
    apps_chat_chat_view,

    # email
    apps_email_inbox_view,
    apps_email_read_view,

    # projects
    apps_projects_list_view,
    apps_projects_details_view,
    apps_projects_gantt_view,
    apps_projects_add_view,

    # social
    apps_social_feed_view,

    # tasks
    apps_tasks_tasks_view,
    apps_tasks_details_view,
    apps_tasks_kanban_view,

    # file manager
    apps_file_manager_view,
)


app_name = "apps"
urlpatterns = [

    # calendar
    path("event/", view=EventListView.as_view(), name="event-list"),
    path("event/add/", view=EventCreateView.as_view(), name="event-add"),
    path("event/edit/<pk>", view=EventUpdateView.as_view(), name="event-edit"),
    path("event/remove/<pk>", view=EventDeleteView.as_view(), name="event-remove"),
    path("calendar", view=apps_calendar_calendar_view, name="calendar"),

    # chat
    path("chat", view=apps_chat_chat_view, name="chat"),

    # email
    path("email/inbox", view=apps_email_inbox_view, name="email.inbox"),
    path("email/read", view=apps_email_read_view, name="email.read"),

    # projects
    path("projects/list", view=apps_projects_list_view, name="projects.list"),
    path("projects/details", view=apps_projects_details_view, name="projects.details"),
    path("projects/gantt", view=apps_projects_gantt_view, name="projects.gantt"),
    path("projects/add", view=apps_projects_add_view, name="projects.add"),

    # social
    path("social/feed", view=apps_social_feed_view, name="social.feed"),

    # tasks
    path("tasks/list", view=apps_tasks_tasks_view, name="tasks.tasks"),
    path("tasks/details", view=apps_tasks_details_view, name="tasks.details"),
    path("tasks/kanban", view=apps_tasks_kanban_view, name="tasks.kanban"),

    # manager
    path("file/manager", view=apps_file_manager_view, name="file.manager")
]

   

