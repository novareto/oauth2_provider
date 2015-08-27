from sanction import Client

# instantiating a client to process OAuth2 response
client = Client(
    token_endpoint="http://karl.novareto.de:8085/token",
    resource_endpoint="http://karl.novareto.de:8085/resource",
    client_id="novareto",
    client_secret="test")

client.request_token(grant_type='client_credentials')
data = client.request('/')
print data
