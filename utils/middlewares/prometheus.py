
from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest
import time


class PrometheusMiddleware(object):
    def __init__(self):
        self.registry = CollectorRegistry()
        self.requests = Counter(
            'falcon_http_request',
            'Counter of total HTTP requests',
            ['method', 'path', 'status'],
            registry=self.registry)

        self.request_historygram = Histogram(
            'falcon_request_latency_seconds',
            'Histogram of request latency',
            ['method', 'path', 'status'],
            registry=self.registry)
        self.up_counter = Counter(
            'up',
            'UP metric',
            registry=self.registry
        )
        self.up_counter.inc(1)
        self.unexpected_errors = Counter(
            'unexpected_errors',
            'Total number of unexpected errors',
            registry=self.registry
        )

    async def process_request(self, req, resp):
        req.start_time = time.time()

    async def process_response(self, req, resp, resource, req_succeeded):
        resp_time = time.time() - req.start_time

        self.requests.labels(method=req.method, path=req.path, status=resp.status).inc()
        self.request_historygram.labels(method=req.method, path=req.path, status=resp.status).observe(resp_time)
        if getattr(resp.context, 'pyexc', -1) != -1:
            self.unexpected_errors.inc()

    async def on_get(self, req, resp):
        data = generate_latest(self.registry)
        resp.text = data.decode('utf-8')
