import traceback
from falcon.response import Response
from falcon.errors import HTTPBadRequest


async def handle_exception(req, resp: Response, ex, params, ws=None):
    if resp is not None:
        resp.status = 200
        resp.media = ex.to_dict(localization=req.context.localization)


async def handle_all_exceptions(req, resp: Response, exc, params, ws=None):
    if resp is not None:
        if isinstance(exc, HTTPBadRequest):
            resp.status = 200
            resp.media = {
                'status': 'ERR',
                'data': {},
                'code': 10,
                'description': exc.description,
                'add_msg': ''
            }
        else:
            print(traceback.format_exc())
            print(str(exc))
            resp.status = 200
            resp.media = {
                'status': 'ERR',
                'data': {},
                'code': 1,
                'description': 'Unexpected error',
                'add_msg': ''
            }
            resp.context.pyexc = exc
            resp.context.trace = traceback.format_exc()
