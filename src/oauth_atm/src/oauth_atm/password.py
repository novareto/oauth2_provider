# -*- coding: utf-8 -*-

import logging
import xmlrpclib
from oauth2 import Provider
from oauth2.error import UserNotAuthenticated
from oauth2.web import ResourceOwnerGrantSiteAdapter
from oauth2.web.wsgi import Application
from oauth2.grant import ResourceOwnerGrant


logging.basicConfig(level=logging.DEBUG)


class TestSiteAdapter(ResourceOwnerGrantSiteAdapter):
    def authenticate(self, request, environ, scopes, client):
        username = request.post_param("username")
        password = request.post_param("password")
        server = "http://localhost:8080/app"
        portal = xmlrpclib.Server(server)
        print server
        if portal.checkAuth(username, password):
            return {'data': 'test'}, username
        raise UserNotAuthenticated
        # A real world application could connect to a database, try to
        # retrieve username and password and compare them against the input
        #if username == "cklinger" and password == "test":
        #    return
#


def make_application(token_store, client_store, token_gen):
    provider = Provider(
        access_token_store=token_store,
        auth_code_store=token_store,
        client_store=client_store,
        token_generator=token_gen)

    provider.add_grant(
        ResourceOwnerGrant(
            expires_in=3600,
            site_adapter=TestSiteAdapter())
    )
    return Application(provider=provider)
