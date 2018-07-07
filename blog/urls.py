from django.urls import register_converter, path

from . import converters, views

register_converter(converters.TwoDigitDayConverter, 'dd')
register_converter(converters.TwoDigitMonthConverter, 'mm')
register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('', views.LatestPostsView.as_view(), name="latest_posts"),
    path('<yyyy:year>/', views.PostsByYearView.as_view(), name="posts_by_year"),
    path('<yyyy:year>/<mm:month>/', views.PostsByYearMonthView.as_view(), name="posts_by_year_month"),
    path('<yyyy:year>/<mm:month>/<dd:day>/', views.PostsByYearMonthDayView.as_view(), name="posts_by_year_month_day"),
    path('<yyyy:year>/<mm:month>/<dd:day>/<title>/', views.PostByYearMonthDayTitleView.as_view(), name="post_by_year_month_day_title"),
    path('tag/<name>/', views.PostsByTagView.as_view(), name="latest_posts_by_tag"),
    path('category/<name>/', views.PostsByCategoryView.as_view(), name="latest_posts_by_category"),
    path('feed/', views.LatestPostsFeed(), name="feed"),
    path('feed/atom/', views.LatestPostsFeedAtom(), name="feed_atom")
]

handler404 = 'blog.views.handler404'
handler500 = 'blog.views.handler500'
