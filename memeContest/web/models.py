from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class MemeContest(models.Model):
    contest_type = models.CharField(
        max_length=50,
        choices=[('contest', 'contest'), ('retweet', 'retweet')])
    contest_id = models.CharField(max_length=100)
    start_date = models.DateTimeField('Start Date')
    end_date = models.DateTimeField('End Date')
    rules = models.TextField()
    prize_1 = models.CharField(max_length=100)
    prize_2 = models.CharField(max_length=100, blank=True, null=True)
    prize_3 = models.CharField(max_length=100, blank=True, null=True)
    posts_limit = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.contest_id}'


class MemeContestPost(models.Model):
    contest_id = models.ForeignKey(MemeContest, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=100)
    twitter_id = models.CharField(max_length=100)
    tweet_url = models.CharField(max_length=1000)
    wallet_address = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f'{self.contest_id}: {self.tweet_url} by {self.twitter_id}'


class RetweetPost(models.Model):
    contest_id = models.ForeignKey(MemeContest, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=100)
    twitter_id = models.CharField(max_length=100)
    tweet_url = models.CharField(max_length=1000)
    wallet_address = models.CharField(max_length=1000, unique=True)

    def __str__(self) -> str:
        return f'{self.contest_id}: {self.tweet_url} by {self.twitter_id}'
