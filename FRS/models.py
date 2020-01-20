from django.db import models


class DialogUser(models.Model):
    uid = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, null=True)
    time_enrolled = models.DateTimeField(null=True)
    photo = models.BinaryField(null=True)
    vector = models.BinaryField(null=True)
    organization = models.CharField(max_length=255, null=True)
    position = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    photo_path = models.CharField(max_length=255, null=True)