from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import MemeContest, MemeContestPost, RetweetPost


def index(request):
    template = 'web/index.html'

    contests_list = MemeContest.objects.all().order_by('-id')

    context = {'contests_list': contests_list}
    return render(request, template, context)


def post_contest(request, contest_id):
    template = 'web/post_twitter.html'
    contest = get_object_or_404(MemeContest, pk=contest_id)

    if contest:
        posts_limit = contest.posts_limit

    participations = MemeContestPost.objects.filter(
        contest_id=contest_id).count()
    context = {
        'contest': contest
    }

    if timezone.now() > contest.end_date or posts_limit and participations >= posts_limit:
        return redirect('web:details', contest_id=contest_id)

    if request.method == 'POST':
        post = request.POST
        if not post['telegram_id'] or not post['twitter_id'] or not post['tweet_url'] or not post['wallet_address']:
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
            newPost.wallet_address = post['wallet_address']

            newPost.save()
            return redirect('web:details', contest_id=contest_id)

    return render(request, template, context)


def post_retweet(request, contest_id):
    template = 'web/post_retweet.html'
    contest = get_object_or_404(MemeContest, pk=contest_id)

    if contest:
        posts_limit = contest.posts_limit

    participations = RetweetPost.objects.filter(
        contest_id=contest_id).count()
    context = {
        'contest': contest
    }

    if timezone.now() > contest.end_date or posts_limit and participations >= posts_limit:
        return redirect('web:details', contest_id=contest_id)

    if request.method == 'POST':
        post = request.POST
        if not post['telegram_id'] or not post['twitter_id'] or not post['tweet_url'] or not post['wallet_address']:
            context['error_message'] = 'A field was missing.'
            return render(request, template, context)
        # Don't allow someone to multiple post its own tweet or wallet multiple times for same contest
        elif RetweetPost.objects.filter(
            (Q(contest_id=contest_id) & (
                Q(
                    tweet_url=post['tweet_url']) | Q(
                    wallet_address=post['wallet_address']))
             )
        ):
            context['error_message'] = 'This tweet url or wallet address has been already registered.'
            return render(request, template, context)
        else:
            newPost = RetweetPost()
            newPost.contest_id = contest
            newPost.telegram_id = post['telegram_id']
            newPost.twitter_id = post['twitter_id']
            newPost.tweet_url = post['tweet_url']
            newPost.wallet_address = post['wallet_address']

            newPost.save()
            return redirect('web:details', contest_id=contest_id)

    return render(request, template, context)


def details(request, contest_id):
    template = 'web/details.html'
    contest = get_object_or_404(MemeContest, pk=contest_id)
    contest_type = contest.contest_type

    if contest_type == 'contest':
        posts = MemeContestPost.objects.filter(
            contest_id=contest).order_by('-id')
    else:
        posts = RetweetPost.objects.filter(contest_id=contest).order_by('-id')

    posts_limit = None
    if posts:
        posts_limit = contest.posts_limit

    participations = posts.count()

    finished = timezone.now() > contest.end_date or (
        posts_limit and participations >= posts_limit)

    context = {'contest_type': contest_type, 'contest': contest,
               'posts': posts, 'finished': finished}
    return render(request, template, context)
