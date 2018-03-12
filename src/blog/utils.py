from django.core.paginator import EmptyPage, PageNotAnInteger


def get_objects_by_page(paginator, page):
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return objects
