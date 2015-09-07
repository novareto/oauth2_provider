# -*- coding: utf-8 -*-

import datetime
from json import dumps
from cgi import parse_qs, escape


def from_timestamp(ts):
    if ts is None:
        return "Never"
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


expired = dumps({
    'error': 'Token expired',
    'error_description': 'The access token has expired.',
})

notfound = dumps({
    'error': 'No such token',
    'error_description': 'The provided access token is invalid.',
})

nonexistant = dumps({
    'error': 'No token provided',
    'error_decription': 'No access token provided in the request.',
})

badrequest = dumps({
    'error': 'Bad Request',
    'error_decription': 'GET request should not have body content.',
})

notallowed = dumps({
    'error': 'Method Not Allowed',
    'error_description': '`verify` method only accepts POST or GET requests.',
})


def verify_app(token_store, client_store):
    def verify(environ, start_response):
        method = environ['REQUEST_METHOD'].lower()
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0

        if method == 'get':
            if request_body_size != 0:
                start_response(
                    '400 Bad Request', [('Content-Type','application/json')])
                return [badrequest]
            else:
                data = parse_qs(environ['QUERY_STRING'])

        elif method == 'post':
            request_body = environ['wsgi.input'].read(request_body_size)
            data = parse_qs(request_body)

        else:
            start_response(
                '405 Method Not Allowed', [('Content-Type','application/json')])
            return [notallowed]

        access_token = data.get('access_token', [None])[0]
        if access_token:
            try:
                access_token = escape(access_token)
                token = token_store.access_tokens[access_token]
                if not token.is_expired():
                    start_response(
                        '200 OK', [('Content-Type','application/json')])
                    return [dumps({
                        'status': 'Token valid',
                        'expiration': from_timestamp(token.expires_at),
                        'client': token.client_id,
                        'userid': token.user_id,
                        'data': token.data,
                    })]
                else:
                    start_response(
                        '401 Unauthorized', [('Content-Type','application/json')])
                    return [expired]
            except KeyError as e:
                start_response(
                    '401 Unauthorized', [('Content-Type','application/json')])
                return [notfound]
        else:
            start_response(
                '401 Unauthorized', [('Content-Type','application/json')])
            return [nonexistant]
    return verify

    
def make_application(token_store, client_store):
    return verify_app(token_store, client_store)
