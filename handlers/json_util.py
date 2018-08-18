import tornado.escape
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class JsonHandler(BaseHandler):
    def _token_check(self, session, CUsers):
        token_db = None
        token = None
        if 'token' in self.request.headers:
            token = self.request.headers['token']
            token_db = session.query(CUsers.token).filter(CUsers.token == token).one_or_none()
            if token_db is not None and token == token_db.token:
                return True
            else:
                message = 'Token not found'
                self.send_error(404, message=message)
        else:
            message = 'Unauthorized'
            self.send_error(401, message=message)

    def prepare(self):
        if self.request.body:
            try:
                self.json_data = tornado.escape.json_decode(self.request.body.decode('utf8'))
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message)  # Bad Request

        self.response = dict()

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'

        self.response = kwargs
        self.write_json()

    def write_json(self):
        output = tornado.escape.json_encode(self.response)
        self.write(output)
