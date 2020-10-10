from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    #the line below takes uers to the new entry page
    path("create_page",views.addEntry, name ="new"),

    #takes users to search results
    path("search/<str:userSearch>", views.search, name ="search"),

    #takes users to edit wiki entry
    path("edit/<str:name>", views.editEntry, name = "edit"),

    # the line below takes users to the appropriate wiki entry with /ENTRY_NAME on URLs
    path("<str:name>", views.showEntry, name = "show"),

]
