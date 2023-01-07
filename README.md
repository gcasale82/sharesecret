![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
##### [sharesecret app demo](https://ijimdb.deta.dev/start "sharesecret app demo")
## Description
**sharesecret** is an app for sharing securely password or secret text on the web. Differently from other apps , sharing happens in 3 steps , for ensuring that only receiver and sender will exchange secrets avoiding public password links on the web. When a password is exposed on the web , also temporary and without a context , it can be used to feed dictionary that then can be used for brute force attacks. Sharesecrets encrypts secret in the browser and store in the database encrypted.Only the receiver with his private key can decrypt the secret.Even if the secure link is stolen secret cannot be retrieved. Share Secret is composed by a FastApi backend webserver and a SQLlite database.
## Usage
1. In the first step receiver user connects to start page and generates RSA keypair (RSA-OAEP 4096 bit) directly in the browser , only the public key is sent to webserver that stores it into the database with the ID.Receiver user will store the private key.A link is generated and is shared with sender user
2. Sender user connects to the shared link and inserts his secret text , the secret is encrypted with receiver user public key in the browser and sent to the webserver that stores it encrypted in the database with ID association.A new link is generated and can be shared with receiver.
3. The receiver connects to the new link and can insert his private key to decrypt the secret.Decryption happens in the browser.
When public key or secret are retrieved at steps 2 or 3 they are deleted from database ; in case steps 2 or 3 happen not suddenly , public key and secret have an expiration timer of 24 hours , then are deleted from database.

When deploying the application , environmet variables can be set , for webserver hostname and TCP port , otherwise default values are used (hostname = 127.0.0.1 and port = 8000).

In the certificates folder the application expects to find  certificate.pem and key.pem for https , otherwise a self signed certificate and key are generated using hostname as common name. 
[![sharesecret worflow](https://raw.githubusercontent.com/gcasale82/sharesecret/main/share-secret-wf.jpg "sharesecret worflow")](https://raw.githubusercontent.com/gcasale82/sharesecret/main/share-secret-wf.jpg "sharesecret worflow")
## Containers
Sharesecret can be deployed using docker or Kubernetes , the official container image can be found at [dockerhub repository](https://hub.docker.com/r/gcasale/sharesecret "dockerhub repository")
. Below an example for deploying the container with ip address 192.168.1.2 and TCP port 8443 : 
### Docker
    docker run -e hosturl=192.168.1.2 -e localport=8443 -p 8443:8443 sharesecret:latest
[![docker](https://github.com/gcasale82/sharesecret/blob/main/sharesecret1.jpg?raw=true "docker")](https://github.com/gcasale82/sharesecret/blob/main/sharesecret1.jpg?raw=true "docker")
### Kubernetes


    kubectl run sharesecret-app --image=gcasale/sharesecret:latest --env="hosturl=192.168.1.2" --env="localport=8443"
[![kubernetes](https://github.com/gcasale82/sharesecret/blob/main/sharesecret2.jpg?raw=true "kubernetes")](https://github.com/gcasale82/sharesecret/blob/main/sharesecret2.jpg?raw=truetp:// "kubernetes")
## Demo
A sharesecret app demo is hosted on deta.io  at this [url](https://ijimdb.deta.dev/start "url") .
The only difference with real app is that this one is using [Deta base](https://docs.deta.sh/docs/base/about/ "Deta base") and not SQLite as database.
