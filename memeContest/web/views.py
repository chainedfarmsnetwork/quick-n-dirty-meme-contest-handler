from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect

from .models import MemeContest, MemeContestPost


def index(request):
    template = 'web/index.html'

    contests_list = MemeContest.objects.all().order_by('-id')

    context = {'contests_list': contests_list}
    return render(request, template, context)


def post(request, contest_id):
    template = 'web/post.html'
    contest = get_object_or_404(MemeContest, pk=contest_id)
    context = {
        'contest': contest
    }

    if timezone.now() > contest.end_date:
        return redirect('web:details', contest_id=contest_id)

    if request.method == 'POST':
        post = request.POST
        if not post['telegram_id'] or not post['twitter_id'] or not post['tweet_url']:
            context['error_message'] = 'A field was missing.'
            return render(request, template, context)
        # Don't allow someone to multiple post its own tweet multiple times
        elif MemeContestPost.objects.filter(tweet_url=post['tweet_url']):
            context['error_message'] = 'This tweet url has been already registered.'
            return render(request, template, context)
        else:
            newPost = MemeContestPost()
            newPost.contest_id = contest
            newPost.telegram_id = post['telegram_id']
            newPost.twitter_id = post['twitter_id']
            newPost.tweet_url = post['tweet_url']

            newPost.save()
            return redirect('web:details', contest_id=contest_id)

    return render(request, template, context)


def details(request, contest_id):
    template = 'web/details.html'
    contest = get_object_or_404(MemeContest, pk=contest_id)
    posts = MemeContestPost.objects.filter(contest_id=contest).order_by('-id')
    finished = timezone.now() > contest.end_date
    context = {'contest': contest, 'posts': posts, 'finished': finished}
    return render(request, template, context)
