# -*- coding: utf-8 -*-

from oauth2 import Provider
from oauth2.web.wsgi import Application
from oauth2.grant import ClientCredentialsGrant


def make_application(token_store, client_store, token_gen):
    auth_controller = Provider(
        access_token_store=token_store,
        auth_code_store=token_store,
        client_store=client_store,
        token_generator=token_gen)

    auth_controller.add_grant(ClientCredentialsGrant())
    return Application(provider=auth_controller)
