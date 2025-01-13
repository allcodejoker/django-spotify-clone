from django.db import models

# Create your models here.

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    gerne = models.CharField(max_length=200)
    audio_url = models.CharField(max_length=300)
    duration = models.CharField(max_length=20)
    cover_image = models.ImageField(upload_to='cover_image/', blank=True, null=True)

    def __str__(self):
        return self.title

    def youtube_url_modify(self):
        if 'youtu.be' in self.audio_url:
            video_id = self.audio_url.split("/")[-1].split("?si=")[0]
        elif "youtube.com" in self.audio_url:
            video_id = self.audio_url.split("v=")[-1].split("&")[0]

        return f"https://www.youtube.com/embed/{video_id}?autoplay=1&controls=0&showinfo=0&autohide=1"
