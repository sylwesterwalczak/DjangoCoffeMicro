import logging
import json
logger = logging.getLogger(__name__)
import logstash

host = 'logstash'

class LogRestMiddleware(object):
    """Middleware to log every request/response.
    Is not triggered when the request/response is managed using the cache
    """
    

    def __init__(self, get_response):
        self.get_response = get_response

    def logger(self, _data):
        test_logger = logging.getLogger('python-logstash-logger')
        test_logger.setLevel(logging.DEBUG)
        test_logger.addHandler(logstash.TCPLogstashHandler(host, 5000, version=1))
        test_logger.info(_data)


    def _log_request(self, request, cached_request_body):
        """Log the request"""
        user = str(getattr(request, 'user', ''))
        method = str(getattr(request, 'method', '')).upper()
        request_path = str(getattr(request, 'path', ''))
        query_params = str(["{}: {}" %(k,v) for k, v in request.GET.items()])
        query_params = query_params if query_params else ''

        data_ = "@req: ({}) [{}] {} {} body:{}".format(user, method, request_path, query_params, cached_request_body) 

        self.logger(data_)

   
    def _log_response(self, request, response):
        """Log the response using values from the request"""
        user = str(getattr(request, 'user', ''))
        method = str(getattr(request, 'method', '')).upper()
        status_code = str(getattr(response, 'status_code', ''))
        status_text = str(getattr(response, 'status_text', ''))
        request_path = str(getattr(request, 'path', ''))
        size = str(len(response.content))
        data_ = "@res:({}) [{}] {} - {} ({} / {})".format(user, method, request_path, status_code, status_text, size) 

        self.logger(data_)

    def __call__(self, request):
        """Method call when the middleware is used in the `MIDDLEWARE` option in the settings (Django >= 1.10)"""
        cached_request_body = getattr(request, 'body', '')
        print(cached_request_body)
        response = self.get_response(request)
        if type(response.content) == bytes and cached_request_body:
            cached_request_body = json.loads(cached_request_body.decode())
        elif cached_request_body:
            cached_request_body = json.loads(cached_request_body)
        else:
            cached_request_body='None'

        self._log_request(request, cached_request_body)
        self._log_response(request, response)

        return response