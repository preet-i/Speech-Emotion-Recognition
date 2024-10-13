from django.db import models

class AudioFile(models.Model):
    audio = models.FileField(upload_to='audio/')
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback from {self.name}"