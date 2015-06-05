[![Container Repository on Quay.io](https://quay.io/repository/coreos/jwt-auth-example/status "Container Repository on Quay.io")](https://quay.io/repository/coreos/jwt-auth-example)

# Quay.io JWT Custom Auth
This repository contains documentation and an example server for Quay.io JWT Custom Authentication.

## JWT Auth protocol

Details about how to implement the JWT auth protocol can be found in the PROTOCOL document.

## To run the example server via Docker:

```
docker run -ti -p 5000:5000 quay.io/coreos/jwt-auth-example
```

## To run the example server directly:

```
python application.py
```

## To test the example server with `curl`:

```
curl --user cooluser:password http://localhost:5000/user/exists
curl --user cooluser:password http://localhost:5000/user/verify
```

