## Quay.io JWT Authentication Protocol

The Quay.io JWT Authentication system allows clients to implement their own custom authentication for self-hosted Quay.io instances. This protocol makes use of [JSON Web Tokens](http://jwt.io) to send verification to Quay.io.

### Required Endpoints

JWT authentication requires two endpoints: one for checking whether a username/e-mail address exists, and one for verifying a (username_or_email, password) pair. Both endpoints make use of *HTTP basic authorization* for passing credentials via the `Authorization` header.

### User Exists endpoint

The user exists endpoint returns whether the specified username/e-mail address exists.

#### Request

```
GET /user/exists/endpoint
Authorization: Basic base64(username:)
```

#### Response if user exists

```
200 OK
```

#### Response if user does not exist

```
404 Not Found
```

### User Verification endpoint

The user verification endpoint returns a signed [JSON Web Tokens](http://jwt.io) if the (username, password) pair matches. If the match fails, it returns an error message indicating the failure.

#### Request

```
GET /user/verify/endpoint
Authorization: Basic base64(username:password)
```

#### Response if user exists and the password matches

```
200 OK
Content-Type: application/json

{
  'token': '(encoded JSON Web Token)'
}
```

##### Constructing the JSON Web Token

The [JSON Web Token](http://jwt.io) returned **must contain** the following claims and must be signed using **RS256** and a private key.

Example:
```
{
  'iss': 'authy',
  'aud': 'quay.io/jwtauthn',
  'nbf': datetime.utcnow(),
  'exp': datetime.utcnow() + timedelta(seconds=60),
  'sub': 'usernamehere',
  'email': 'email@address.com'
}
```

| Claim  | Value                                                                         |
| ------ | ----------------------------------------------------------------------------- |
| iss    | The issuer of this token. Must match that defined in the Quay.io config       |
| aud    | The intended audience for the token. Must be 'quay.io/jwtauthn'               |
| nbf    | The time before which the token is not valid. UTC Now, in seconds since epoch |
| exp    | When the token expires. No later than UTC Now + 300 seconds (since epoch)     |
| sub    | The username for the verified user.                                           |
| email  | The e-mail address of the verified user.                                      |


#### Response if user does not exists or the password does not match

```
4XX
Error message to display to the user
```