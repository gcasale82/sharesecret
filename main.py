from os import environ , path
import uvicorn
#environment variables are hosturl , localport
#export hosturl='127.0.0.1' ; export localport=8000
try : localport = environ['localport']
except : localport = "8000"

if (path.exists("./certificates/certificate.pem") and path.exists("./certificates/key.pem")):
    pass
else :
    exec(open('generate_certificate.py').read())
uvicorn.run("run:app", host="0.0.0.0", port=int(localport), log_level="debug",reload=False,ssl_keyfile="./certificates/key.pem",ssl_certfile="./certificates/certificate.pem")