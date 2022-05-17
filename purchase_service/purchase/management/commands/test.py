from django.core.management.base import BaseCommand, CommandError
import logging
import logstash
import sys

import logging
logger = logging.getLogger(__name__)

host = 'logstash'


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        test_logger = logging.getLogger('python-logstash-logger')
        test_logger.setLevel(logging.DEBUG)
        # test_logger.addHandler(logstash.LogstashHandler(host, 5000, version=1))
        test_logger.addHandler(logstash.TCPLogstashHandler(host, 5000, version=1))
        # add extra field to logstash message
        extra = {
            'test_string': 'python version: ' + repr(sys.version_info),
            'test_boolean': True,
            'test_dict': {'a': 1, 'b': 'c'},
            'test_float': 1.23,
            'test_integer': 123,
            'test_list': [1, 2, '3'],
        }
        test_logger.info('python-logstash: test extra fields', extra=extra)
        self.stdout.write(self.style.SUCCESS("ok"))
