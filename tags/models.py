from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # todo To define a generic rel. we need 3 fields:
    # Type -> Product, article, Collection, Video..etc
    # ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
