from django.core.paginator import EmptyPage, PageNotAnInteger


def get_objects_by_page(paginator, page):
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return objects, objects.has_other_pages()

def generate_archive(posts):
    archive = {}
    for post in posts:
        year = post.pub_date.strftime('%Y')
        month = post.pub_date.strftime('%B')
        if year not in archive:
            archive[year] = {
                "number_of_posts": 0,
                "months": {}
            }
        
        if month not in archive[year]["months"]:
            archive[year]["months"][month] = {
                "month_number": post.pub_date.month,
                "number_of_posts": 0,
                "posts": []
            }

        archive[year]["number_of_posts"] += 1
        archive[year]["months"][month]['number_of_posts'] += 1
        archive[year]["months"][month]['posts'].append(post)

    return archive
