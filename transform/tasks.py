# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import os
import logging
import commands
import time

from django.db.models import ObjectDoesNotExist
from django.conf import settings
from celery import shared_task
from transform.models import Transform
from transform.exceptions import TransformException

logger = logging.getLogger(__name__)


@shared_task(name='transform.transform_file')
def transform_file(pk, filename):
    time.sleep(1)
    try:
        transform = Transform.objects.get(pk=pk)
    except ObjectDoesNotExist:
        logger.warning('transform failed, cannot find transform object in model with pk=%s', pk)
        return
    transform.status = Transform.STATUS_RUNNING
    transform.save()

    try:
        transform_file_execute(filename=os.path.join(settings.MEDIA_ROOT, filename))
    except Exception as e:
        logger.warning('transform failed', exc_info=1)
        transform.status = Transform.STATUS_FAIL
        transform.error_message = str(e)
        transform.save()
        return
    transform.final.name = filename + '.epub'
    transform.status = Transform.STATUS_FINISHED
    transform.save()


def transform_file_execute(filename):
    command = '/usr/local/bin/convertio --apikey %s -f epub -o %s %s' % (
        settings.CONVERTIO_API_KEY,
        os.path.dirname(filename),
        filename,
    )
    result_filename = filename + '.epub'
    status, output = commands.getstatusoutput(command)
    if status != 0 or 'Done! => %s' % result_filename not in output:
        raise TransformException("cannot transform file %s. %s" % (filename, output))
    return result_filename