# HTTPS Uvicorn Server with Self-Signed Certificate

This guide will walk you through the following steps:
1. Create a self-signed certificate.
2. Use the certificate to start a Uvicorn HTTPS server.
3. Invoke the HTTPS server using a Python client.

## 1. Create a Self-Signed Certificate

To create a self-signed certificate for `localhost` and `127.0.0.1`, follow these steps:

### Using PowerShell:

1. Open **PowerShell as Administrator**.
2. Run the following command to create a self-signed certificate with `localhost` and `127.0.0.1` as the **Subject Alternative Names (SAN)**:

   ```powershell
   $cert = New-SelfSignedCertificate -DnsName "localhost", "127.0.0.1" -CertStoreLocation "cert:\LocalMachine\My" -NotAfter (Get-Date).AddYears(1) -FriendlyName "Localhost HTTPS Cert" -KeyExportPolicy Exportable -KeySpec Signature -KeyLength 2048 -HashAlgorithm SHA256
3. Export the certificate to a .pfx file:

   ```powershell
   Export-PfxCertificate -Cert $cert -FilePath "C:\path\to\cert.pfx" -Password (ConvertTo-SecureString -String "YourPassword" -Force -AsPlainText)
4. Use OpenSSL to convert the .pfx file into cert.pem (certificate) and key.pem (private key):
   1. Extract the private key:
   ```powershell
   openssl pkcs12 -in cert.pfx -nocerts -out key.pem -nodes
   ```
   2. Extract the certificate:
   ```powershell
   openssl pkcs12 -in cert.pfx -clcerts -nokeys -out cert.pem
   ```
   Now you have cert.pem and key.pem files, which will be used to run your HTTPS server.

## 2. Start a Uvicorn HTTPS Server
Start the Uvicorn server with the SSL certificate and key:

   ```powershell
   uvicorn fastapi_demo:app --host 127.0.0.1 --port 8000 --ssl-certfile=cert.pem --ssl-keyfile=key.pem
   ```
The server will now be running on https://127.0.0.1:8000/.

## 3. Invoke the HTTPS Server Using a Python Client
   ```powershell
   python client.py
   ```




