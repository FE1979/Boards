from django.db import models

# Create your models here.
class Thread(models.Model):
    """ Main table with a list of threads """

    pinned = models.BooleanField()
    thread_id = models.PositiveIntegerField(primary_key=True)
    author_name = models.CharField(max_length=256)
    author_link = models.URLField()
    title = models.CharField(max_length=256)
    Update_date = models.DateField(auto_now=False)
    url = models.URLField()


class Post(models.Model):
    """ Text information in the thread """

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    text = models.TextField()
    post_date = models.DateField(auto_now=False)


class Attachment(models.Model):
    """ references to any attachments in the thread """

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    url = models.URLField()
