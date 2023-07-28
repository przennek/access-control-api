#!/bin/zsh

# Create a directory to store the certificates
mkdir ssl_certificates
cd ssl_certificates || exit

# Generate a private key
openssl genpkey -algorithm RSA -out server.key

# Generate a certificate signing request (CSR)
openssl req -new -key server.key -out server.csr

# Generate a self-signed certificate valid for 365 days
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

# PEM for curl see: source.this
openssl x509 -in server.crt -out server.pem -outform PEM