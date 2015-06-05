import jwt
import base64

from flask import Flask, abort, jsonify, request, make_response
from datetime import datetime, timedelta

_FAKE_USERS = [
  {'username': 'cooluser', 'email': 'user@domain.com', 'password': 'password'},
  {'username': 'some.neat.user', 'email': 'neat@domain.com', 'password': 'foobar'}
]

def _get_basic_auth():
  data = base64.b64decode(request.headers['Authorization'][len('Basic '):])
  return data.split(':', 1)


app = Flask('fakeauth')

@app.route('/user/exists', methods=['GET'])
def user_exists():
  # Decode the Authorization header. In this call, it will have the form:
  # Basic base64(username:)
  username, _ = _get_basic_auth()

  # Find the user entry with the matching username or e-mail address.
  for user in _FAKE_USERS:
    if user['username'] == username or user['email'] == username:
      return 'OK'

  abort(404)

@app.route('/user/verify', methods=['GET'])
def verify_user():
  # Load the private key. In a real implementation, this would be cached.
  with open('example_private.key', 'rb') as f:
    private_key = f.read()

  # Decode the Authorization header. In this call, it will have the form:
  # Basic base64(username:password)
  username, password = _get_basic_auth()

  # You can return a custom error message by returning it as the contents of the 4XX error.
  if username == 'disabled':
    return make_response('User is currently disabled', 401)

  # Find the user entry with the matching username or e-mail address.
  for user in _FAKE_USERS:
    if user['username'] == username or user['email'] == username:
      # Verify the user's password.
      if password != user['password']:
        return make_response('', 404)

      # Note that all these fields are required:
      #  iss - The issuer, which should match that defined in your configuration
      #  aud - Must be 'quay.io/jwtauthn'
      #  nbf - The current time when the token was minted
      #  exp - The time when token expires. Must not be greater than five minutes from now.
      #  sub - The user's username.
      #  email - The user's e-mail address.
      token_data = {
        'iss': 'authy',
        'aud': 'quay.io/jwtauthn',
        'nbf': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=60),
        'sub': user['username'],
        'email': user['email']
      }

      # RS256 is required as the encryption type.
      encoded = jwt.encode(token_data, private_key, 'RS256')
      return jsonify({
        'token': encoded
      })

  return make_response('', 404)

app.config['TESTING'] = True
app.config['DEBUG'] = True


def run_example_server():
  app.run(port=5000, debug=True, threaded=True, host='0.0.0.0')

if __name__ == '__main__':
  run_example_server()