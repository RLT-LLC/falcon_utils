import time
import logging
from logging.handlers import RotatingFileHandler
import json
from falcon.asgi import Request, Response
from datetime import datetime, timezone

kibana_formatter = logging.Formatter("[log_start]\n%(message)s")
kibana_handler = RotatingFileHandler(F'./logs/requests{datetime.now().strftime("%d.%m.%Y")}.log', maxBytes=204800,
                                     encoding="utf-8")
kibana_handler.setFormatter(kibana_formatter)
kibana_logger = logging.getLogger('requests_logger')
kibana_logger.addHandler(kibana_handler)
kibana_logger.setLevel(logging.DEBUG)


class LoggingMiddleware:
    def __init__(self, project, server_name):
        self.project = project
        self.server_name = server_name

    async def process_request(self, req: Request, resp: Response):
        req.context.start_time = time.time()

    async def process_response(self, req: Request, resp: Response, resource, req_succeeded):
        if req.uri.endswith('metrics'):
            return
        if req.method == 'POST':
            req_data = await req.get_media()
        else:
            req_data = {}
        dt = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        if getattr(resp.context, 'pyexc', -1) != -1:
            exc = type(resp.context.pyexc).__name__
            trace = resp.context.trace
            level = 'ERR'
        else:
            exc = ''
            trace = ''
            level = 'OK'

        if req.context.get('jwt_body'):
            user_info = {
                "id": str(req.context.get('jwt_body').get('user_id')),
                "human_readable": req.context.get('jwt_body').get('identity')
            }
        else:
            user_info = {
                "id": "someid",
                "human_readable": "somehumanreadable"
            }

        try:
            logging_request_json = json.dumps(req_data)
        except TypeError as e:
            print("Cannot cast request payload to an json object", e)
            logging_request_json = "Cannot parse payload"

        msg = {
            "common": self.project,
            "server_name": self.server_name,
            "nginx_request_id": req.headers.get('x-request-id', 'noxrequestidheader'),
            "userinfo": user_info,
            "date": dt,
            "url": req.relative_uri,
            "time": dt,
            "level": level,
            "request": logging_request_json,
            "response_code": resp.media.get('exc', {}).get('code', 0) if resp.media else 0,
            "response": json.dumps(resp.media) if resp.media else "",
            "traceback": trace,
            "exception": exc,
            "timedelta": round(time.time() - req.context.start_time, 3),
            "headers": json.dumps(req.headers)
        }
        for name in ['baggage', 'sentry-trace']:
            msg[name] = req.headers.get(name, None)
        kibana_logger.info(json.dumps(msg))
