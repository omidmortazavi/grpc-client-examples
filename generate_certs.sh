#!/bin/bash

# Create the certificates directory if it doesn't exist
mkdir -p certificates

# Generate a Certificate Authority (CA) Key and Certificate
openssl genpkey -algorithm RSA -out certificates/ca.key
openssl req -new -x509 -days 365 -key certificates/ca.key -out certificates/ca.crt -subj "/CN=Certificate Authority"

echo "Generated CA Key (ca.key) and Certificate (ca.crt)"

# Generate the Server Key and Certificate Signing Request (CSR)
openssl genpkey -algorithm RSA -out certificates/server.key
openssl req -new -key certificates/server.key -out certificates/server.csr -subj "/CN=localhost"

echo "Generated Server Key (server.key) and Certificate Signing Request (server.csr)"

# Sign the Server CSR with the CA Certificate
openssl x509 -req -days 365 -in certificates/server.csr -CA certificates/ca.crt -CAkey certificates/ca.key -CAcreateserial -out certificates/server.crt -extensions v3_req -extfile <(printf "[v3_req]\nsubjectAltName=DNS:localhost,IP:127.0.0.1")

echo "Signed Server CSR with the CA Certificate. Generated Server Certificate (server.crt)"

# Generate the Client Key and Certificate Signing Request (CSR)
openssl genpkey -algorithm RSA -out certificates/client.key
openssl req -new -key certificates/client.key -out certificates/client.csr -subj "/CN=Client"

echo "Generated Client Key (client.key) and Certificate Signing Request (client.csr)"

# Sign the Client CSR with the CA Certificate
openssl x509 -req -days 365 -in certificates/client.csr -CA certificates/ca.crt -CAkey certificates/ca.key -CAcreateserial -out certificates/client.crt

echo "Signed Client CSR with the CA Certificate. Generated Client Certificate (client.crt)"

# Cleanup the CSR and serial files
rm -f certificates/server.csr certificates/client.csr certificates/ca.srl 2>/dev/null

echo "Cleanup: Removed Certificate Signing Requests (server.csr, client.csr) and CA Serial File (ca.srl)"
