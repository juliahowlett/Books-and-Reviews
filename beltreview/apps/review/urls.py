from django.conf.urls import url
from . import views    

urlpatterns = [
	url(r'^$', views.index),
	url(r'^index$', views.index),
	url(r'^reviews/index$', views.index),
	url(r'^create_user$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^dashboard$', views.dashboard),
	url(r'^show_reviewer/(?P<book_id>\d+)/$', views.show_reviewer),
	url(r'^show_review/(?P<book_id>\d+)/$', views.show_reviews),
	url(r'^add_book$', views.add_book),
	url(r'^new_book$', views.new_book),
	url(r'^add_review/(?P<quote_id>\d+)$', views.add_review),
	url(r'^remove_review/(?P<quote_id>\d+)$', views.remove_review)
]	