from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.core.checks.messages import CheckMessage
from django.db import models


class User(AbstractUser):
    pass

class Tags(models.Model):
    tag1 = models.CharField(max_length=50)
    type = models.IntegerField()



class Talks(models.Model):
    language_choices = [
        ("", "Language"),
        ("Spanish","Spanish"),
        ("English", "English"), 
        ("French", "French"), 
        ("Russian", "Russiian"), 
        ("Italian", "Italian"), 
        ("German", "German"), 
        ("Indi", "Indi"),
        ("Chinese", "Chinese"), 
        ("Japanase", "Japanese"), 
        ("Arabian", "Arabian"), 
        ("Other", "Other")
    ]

    difficulty_choices = [
        ("", "Difficulty"),
        ("Introductory", "Introductory"), 
        ("Intermediate", "Intermediate"), 
        ("Advanced", "Advanced")
    ]

    duration_choices = [
        ("", "Duration"), 
        ("-30", "<30min"), 
        ("30-1", "30min-1h"),
        ("1-1.5", "1h-1.5h"),
        ("2-2.5", "2h-2.5h"),
        ("2.5-3", "2.5h-3h"),
        ("+3", ">3h")
    ]


    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator") 
    date = models.DateField()

    description = models.CharField(max_length=5000)
    title = models.CharField(max_length=100)

    max_people = models.IntegerField()

    language = models.CharField(choices=language_choices, max_length=64)
    difficulty = models.CharField(choices=difficulty_choices, max_length=64)


    talk_date = models.DateField()
    start_hour = models.TimeField()
    duration = models.CharField(blank=True, null=True, max_length=64, choices=duration_choices)

    image = models.CharField(max_length=64, blank=True, null=True)

    tags = models.ManyToManyField(Tags, related_name="tags1", blank=True, null=True)

    about_author = models.CharField(max_length=1000)
    prerrequesites = models.CharField(max_length=1000)

    how_to_attend_meeting = models.CharField(max_length=1000)

    attendants = models.ManyToManyField(User, related_name="attendants")


    def get_language(self):
        return self.language_choices

    def get_difficulty(self):
        return self.difficulty_choices

    def get_duration(self):
        return self.duration_choices

    def serialize(self):
        return {
            "creator": self.creator.username, 
            "date": self.date, 
            "description": self.description, 
            "title":self.title,
            "max_people":self.max_people,
            "language":self.language,
            "difficulty":self.difficulty,
            "talk_date":self.talk_date,
            "start_hour": self.start_hour,
            "duration": self.duration,
            "image":self.image,
            "tags":[tag.tag1 for tag in self.tags.all()],
            "prerrequesites":self.prerrequesites,
            "about_author": self.about_author,
            "how_to_attend_meeting":self.how_to_attend_meeting
        }
