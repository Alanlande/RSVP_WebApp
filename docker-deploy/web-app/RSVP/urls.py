from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('homepage/', views.EventHomepage, name='homepage'),
    path('create-event/', views.createEvent, name='create-event'),
    path('event-hompage/', views.EventHomepage, name='event-hompage'),

    path('owner-event/', views.OwnerEvent, name='event-owner'),
    path('guest-event/', views.GuestEvent, name='event-guest'),
    path('vendor-event/', views.VendorEvent, name='event-vendor'),

    path('owner/<int:event_id>/', views.ownerPage, name='owner-page'),
    path('vendor/<int:event_id>/', views.vendorPage, name='vendor-page'),
    path('guest/<int:event_id>/', views.guestPage, name='guest-page'),
    path('guestPlusOne/<int:event_id>/', views.guestPlusOnePage, name='guestPlusOne-page'),
    path('view-answer/<int:event_id>/', views.viewAnswerPage, name='view-answer-page'),
    path('invite/<int:event_id>/', views.invitePage, name='invite-page'),
    path('create-choice/<int:question_id>', views.createChoice, name='choice-create-page'),
    path('create-question/<int:event_id>', views.createQuestion, name='question-create-page'),
    path('finalize-question/<int:question_id>', views.finalizeQuestion, name='finalize-page'),
    path('free-text-response/<int:question_id>', views.freeText, name='free-text-page'),
    path('edit-question/<int:question_id>', views.editQuestion, name='question-edit-page'),
    path('edit-choice/<int:choice_id>', views.editChoice, name='choice-edit-page'),
    path('delete-question/<int:question_id>', views.deleteQuestion, name='question-delete-page'),
    path('delete-choice/<int:choice_id>', views.deleteChoice, name='choice-delete-page'),
    path('pendingPage/<int:role_id>', views.pendingPage, name='pendingPage'),
]