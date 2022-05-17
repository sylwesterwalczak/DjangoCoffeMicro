import logstash
import logging
import json
logger = logging.getLogger(__name__)

host = 'logstash'


class LogRestMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def logger(self, data):
        """Send to logstash"""

        _logger = logging.getLogger('python-logstash-logger')
        _logger.setLevel(logging.DEBUG)
        _logger.addHandler(logstash.TCPLogstashHandler(host, 5000, version=1))
        _logger.info(data)

    def _log_request(self, request, cached_request_body):
        """Log the request"""
        user = str(getattr(request, 'user', ''))
        method = str(getattr(request, 'method', '')).upper()
        request_path = str(getattr(request, 'path', ''))
        query_params = str(["{}: {}" % (k, v) for k, v in request.GET.items()])
        query_params = query_params if query_params else ''

        data = "@req: ({}) [{}] {} {} body:{}".format(
            user,
            method,
            request_path,
            query_params,
            cached_request_body
        )

        self.logger(data)

    def _log_response(self, request, response):
        """Log the response using values from the request"""
        user = str(getattr(request, 'user', ''))
        method = str(getattr(request, 'method', '')).upper()
        status_code = str(getattr(response, 'status_code', ''))
        status_text = str(getattr(response, 'status_text', ''))
        request_path = str(getattr(request, 'path', ''))
        size = str(len(response.content))
        data = "@res:({}) [{}] {} - {} ({} / {})".format(
            user,
            method,
            request_path,
            status_code,
            status_text,
            size
        )

        self.logger(data)

    def catch_request_body(self, response,  cached_request_body):
        """Fetch request body"""

        if type(response.content) == bytes and cached_request_body:
            cached_request_body = json.loads(cached_request_body.decode())
        elif cached_request_body:
            cached_request_body = json.loads(cached_request_body)
        else:
            cached_request_body = 'None'

    def __call__(self, request):

        _request_body = getattr(request, 'body', '')
        response = self.get_response(request)

        cached_request_body = self.catch_request_body(response, _request_body)

        self._log_request(request, cached_request_body)
        self._log_response(request, response)

        return response
