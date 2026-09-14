import os
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    color = models.CharField(max_length=7, default='#3B82F6')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(
        'Category', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='notes'
    )
    service_date = models.DateField(default=timezone.now, help_text="Date of the service/event")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class NoteAttachment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='note_attachments/%Y/%m/%d/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_image(self):
        return self.file.name.lower().endswith(('.png', '.jfif', '.jpg', '.jpeg', '.gif', '.webp'))

    @property
    def file_name(self):
        return os.path.basename(self.file.name)

    @property
    def extension(self):
        return os.path.splitext(self.file.name)[1].lstrip('.').upper()