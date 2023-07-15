from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from blog.models import Post
from django.shortcuts import redirect
from blog.forms import CommentForm
import logging
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_cookie
# Add logger

logger = logging.getLogger(__name__)

def index(request):
  # {{ post.published_at|date:"M, d Y" }}, {{ value|lower }}

    posts = Post.objects.filter(published_at__lte=timezone.now())
    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})



def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    logger.info(
    "Created comment on Post %d for user %s", post.pk, request.user
    )
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None

    return render(
        request, "blog/post-detail.html", {"post": post, "comment_form": comment_form}
    )

#logger.debug("Created user %s with email %s" % (username, email)) # Bad
#logger.debug("Created user %s with email %s", username, email) # Better
#logger.debug("Created user %s with email %s", username, email, extra={"username": username, "email": email}) # Best
#logger.log(logging.DEBUG, "Created user %s with email %s", username, email)
#logger.debug("Created user %s with email %s", username, email, extra={"username": username, "email": email})


"""
try:
    # some code that might raise an exception
    raise_exception()
except ValueError:
    logger.exception("An exception occured")
    
    
try:
    answer = 9 / 0
    print(f"The answer is: {answer}")
    raise_exception()
except ZeroDivisionError:
    logger.exception("A divide by zero exception occured")
    
    
"""

"""
# write this function without a decorator
def index(request):
    from django.http import HttpResponse
    return HttpResponse(str(request.user).encode("ascii"))
    posts = Post.objects.filter(published_at__lte=timezone.now())
    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})

# open the normal browser and ingonito browser and compare the results

# then add the decorator # @cache_page(60 * 15) # 15 minutes
# then refresh the normal browser and ingonito browser and compare the results
# i should see the same results in both browsers because the cache is in the server not in the browser
"""

"""
# adding vary_on_cookie decorator in order to cache the page for each user
# because i want to avoid caching the page for a user and then serving it to another user with the
# same data for the first user

# @cache_page(300)
# @vary_on_cookie
# def index(request):
#     from django.http import HttpResponse
#     return HttpResponse(str(request.user).encode("ascii"))
#     posts = Post.objects.filter(published_at__lte=timezone.now())
#     logger.debug("Got %d posts", len(posts))
#     return render(request, "blog/index.html", {"posts": posts})

"""