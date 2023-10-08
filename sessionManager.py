import uuid
from functools import cached_property
from http.cookies import SimpleCookie


def get_session(obj):
    c = obj.cookies
    if not c:
        c = SimpleCookie()
        c["session"] = uuid.uuid4()
    elif not c.get("session"):
        c = SimpleCookie()
        c["session"] = uuid.uuid4()
    else:
        print("Cookie found")
        
    return c.get("session").value

def set_book_cookie(obj, session_id, max_age=10):
    c = SimpleCookie()
    c["session"] = session_id
    c["session"]["max-age"] = max_age
    obj.send_header('Set-Cookie', c.output(header=''))


    
    