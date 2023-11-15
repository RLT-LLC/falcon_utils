import re
from falcon.asgi import Request, Response
from utils.errors import ExceptionCodes, CustomHTTPError
from ..base_resources import BaseResource

pattern = r"^Token (?P<token>.*)$"


class AuthMiddleware:
    async def process_resource(
            self, req: Request, _resp: Response, resource: BaseResource, _params):

        req.context.localization = req.headers.get("localization", "")
        if not resource.require_auth:
            return
        token = req.headers.get("authorization", "")
        match = re.match(pattern, token)
        if match is None:
            raise CustomHTTPError(ExceptionCodes.NoAdminToken)
        token = match.group("token")
        req.context.profile = await resource.mongo.get_user_by_token(token)
        # await resource.mongo.update_online(req.context.profile['_id'])
