
import logging
import jwt
from pyramid.httpexceptions import HTTPUnauthorized

logger = logging.getLogger(__name__)

def logging_middleware(handler, registry):
    def logging_handler(request):
        response = handler(request)

     
        logger.info(f"{request.method} {request.path} - {response.status_code}")

        return response

    return logging_handler


def expiration_middleware(handler, registry):
    def expiration_handler(request):
        response = handler(request)


        token = request.headers.get('Authorization')
        if token:
            try:
                decoded_token = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
                exp_time = datetime.datetime.fromtimestamp(decoded_token['exp'])
                now = datetime.datetime.utcnow()
                if now > exp_time:
                    return HTTPUnauthorized("Token has expired.")
            except jwt.ExpiredSignatureError:
                return HTTPUnauthorized("Token has expired.")

        return response

    return expiration_handler

