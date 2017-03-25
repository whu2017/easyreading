# -*- coding: utf-8 -*-

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.transform.models import Transform
from app.transform.tasks import transform_file

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Transform)
def transform_handler(sender, instance, created, **kwargs):
    if created:
        transform_file.apply_async(args=[instance.pk, instance.origin.name], kwargs={})
