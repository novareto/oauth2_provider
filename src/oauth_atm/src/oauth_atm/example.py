# -*- coding: utf-8 -*-

import cherrypy
from . import verify, client_credentials, password
from oauth2.tokengenerator import Uuid4
from oauth2.store.memory import ClientStore, TokenStore

tokens = TokenStore()
clients = ClientStore()
clients.add_client(client_id="novareto", client_secret="test",
                        redirect_uris=[])

tickets = Uuid4()
tickets.expires_in['client_credentials'] = 7200


def run():
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8085,
    })

    cherrypy.tree.graft(
        client_credentials.make_application(tokens, clients, tickets),
        '/auth.client')

    cherrypy.tree.graft(
        password.make_application(tokens, clients, tickets),
        '/auth.passwd')

    cherrypy.tree.graft(
        verify.make_application(tokens, clients),
        '/verify')
    
    cherrypy.engine.start()
    cherrypy.engine.block()
