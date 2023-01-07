# sharesecret
sharesecret is an app for sharing securely password or secret text on the web.
Differently from other apps , sharing happens in 3 steps , for ensuring that only receiver and sender will exchange secrets avoiding public password links on the web.
When a password is exposed on the web , also temporary and without a context , it can be used to feed dictionary that then can be used for brute force attacks.
Sharesecrets encrypts secret in the browser and store in the database encrypted.Only the receiver with his private key can decrypt the secret.Even if the secure link is stolen secret cannot be retrieved.
