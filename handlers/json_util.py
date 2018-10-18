import tornado.escape
import tornado.web
from database_tools.alchemy import CUsers
import hashlib
from salt import salt
from datetime import datetime, timedelta


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class JsonHandler(BaseHandler):
    def _create_sha(self, string):
        return hashlib.sha256(string.encode() + salt.encode()).hexdigest()

    def _get_elements(self, session, CElem):
        elem_set = session.query(CElem).all()

        for elem in elem_set:
            self.write(str(elem) + "\n")

    def _get_filtered(self, session, CElem, uid):
        elem_set = session.query(CElem).filter_by(uid=uid).all()

        for elem in elem_set:
            self.write(str(elem) + "\n")

    def _token_expiration(self):
        today = datetime.now()
        days = timedelta(days=5)
        token_expire = (today + days)
        return token_expire

    def _token_check(self):
        session = self.db
        token_db = None
        token = None
        if 'token' in self.request.headers:
            token = self.request.headers['token']
            query_db = session.query(CUsers).filter(CUsers.token == token).one_or_none()
            if query_db is not None and token == query_db.token:
                if query_db.tokenexp is None:
                    self.set_status(401, reason='Your token expired')
                else:
                    token_expiration_timestamp = query_db.tokenexp.timestamp()
                    if token_expiration_timestamp < datetime.today().timestamp():
                        self.set_status(401, reason='Your token expired')
                    else:
                        return query_db
            else:
                message = 'Token not found'
                self.set_status(404, reason=message)
        else:
            message = 'Unauthorized'
            self.set_status(401, reason=message)



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
