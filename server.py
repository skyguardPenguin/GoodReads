from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
import re
import redis
import uuid 
import util
import htmlBuilder
import sessionManager
import searchManager

r = redis.Redis(host='localhost', port=6379, db=0)

class WebRequestHandler(BaseHTTPRequestHandler):
        @cached_property
        def url(self):
            return urlparse(self.path)

 
        @cached_property
        def cookies(self):
            return SimpleCookie(self.headers.get("Cookie"))
        
        def get_index(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            sessionId = sessionManager.get_session(self)
            sessionManager.set_book_cookie(self, sessionId)
            self.end_headers()
            template = r.get('index').decode()
            content = htmlBuilder.getIndexContent(template)
            self.wfile.write(content.encode("utf-8"))

        def get_book(self, book_id):
            sessionId = sessionManager.get_session(self)
            book_recomendation = self.get_book_recomendation(sessionId,book_id)
            template = f""" 
                {r.get("book").decode()}

                
                ---------------------------------------
                <p>  URL: {self.url}              </p>
                <p>  Sesión: {sessionId}      </p>
                <p>  Recomendación: {book_recomendation}</p>
                """
            content = htmlBuilder.getBookContent(template, book_id)

            if content:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                sessionManager.set_book_cookie(self,sessionId)
                self.end_headers()

                print(content.encode("UTF-8"))
                self.wfile.write(content.encode("UTF-8"))
            else:
                self.send_error(404, "Not Found")


        def text_search(self, pattern):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            sessionId = sessionManager.get_session(self)
            sessionManager.set_book_cookie(self, sessionId)
            self.end_headers()
            template = r.get('index').decode()
            match_list = searchManager.search_sentence(r,pattern)
            content = htmlBuilder.getSearchContent(template,match_list)
            self.wfile.write(content.encode("utf-8"))            


        def get_book_recomendation(self, session_id, book_id):
            r.rpush(session_id,book_id)
            books = r.lrange(session_id,0,5)
            all_books = [str(i+1) for i in range(4)]
            new = [b for b in all_books if b not in
               [vb.decode() for vb in books]]
            
            if new:
                return new[0]
            else:
                return 0

        def do_GET(self):
            params =""
            if(self.url.query):
                params="?" +self.url.query

            method = self.get_method(self.url.path + params)
            if method:
                method_name, dict_params = method
                method = getattr(self, method_name)
                method(**dict_params)
                return
            else:
                self.send_error(404, "Not Found")

        def get_method(self, path):
            for pattern, method in mapping:
                match = re.match(pattern, path)
                print("path:  " + path)
                if match:
                    return (method, match.groupdict())
             

mapping = [
            (r'^/books/(?P<book_id>\d+)$', 'get_book'),
            (r'^/$', 'get_index'),
            (r'^/search\?pattern=(?P<pattern>.+)$', 'text_search')
        ]

if __name__ == "__main__":
    print("Server starting...")
    server = HTTPServer(("localhost", 8080), WebRequestHandler)
    server.serve_forever()