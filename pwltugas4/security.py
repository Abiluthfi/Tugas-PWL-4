
from pyramid.security import Allow, Authenticated, Everyone

class RootACL:
    __acl__ = [
        (Allow, Authenticated, 'view'),
        (Allow, 'admin', 'edit'),
    ]

def groupfinder(userid, request):
    user = DBSession.query(User).filter_by(id=userid).first()
    if user:
        return ['admin']
