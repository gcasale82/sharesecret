from typing import List , Callable , Optional , Awaitable
import databases
import sqlalchemy
from fastapi import FastAPI , Request , HTTPException
from fastapi.responses import HTMLResponse , FileResponse
from pydantic import BaseModel
from datetime import datetime
import asyncio
from functools import wraps
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./secret_database.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

secrets = sqlalchemy.Table(
    "secrets",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("ciphertext", sqlalchemy.String),
    sqlalchemy.Column("timestamp" , sqlalchemy.Integer )
)

public_keys_table = sqlalchemy.Table(
    "publickeys",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("publickey" , sqlalchemy.String ),
    sqlalchemy.Column("timestamp" , sqlalchemy.Integer )
)
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class SecretIn(BaseModel):
    ciphertext: str
    id: str


class SecretOut(BaseModel):
    id: str
    ciphertext: str

class PublicKey(BaseModel):
    id:str
    publickey:str 

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/doc_image")
async def doc_image():
    return FileResponse("share-secret-wf.jpg")

@app.get("/documentation", response_class=HTMLResponse)
async def doc_page(request: Request):
    return templates.TemplateResponse("doc.html",{"request": request})

@app.get("/start", response_class=HTMLResponse)
async def start_page(request: Request):
    return templates.TemplateResponse("start.html",{"request": request})



@app.get("/secrets/{item_id}", response_class=HTMLResponse)
async def read_secrets(request: Request, item_id : str):
    query = secrets.select().where(secrets.columns.id==item_id)
    result = await database.fetch_all(query)
    await database.execute(secrets.delete().where(secrets.columns.id==item_id))
    if not result :
        raise HTTPException(status_code=404,detail="Item not found",headers={"X-Error": "The item is missing or previously deleted"},)
    return templates.TemplateResponse("deliver.html", {"request": request, "id": result[0][0] , "ciphertext" : result[0][1]})

@app.get("/sendsecret/{item_id}", response_class=HTMLResponse)
async def read_keyss(request: Request, item_id : str):
    query = public_keys_table.select().where(public_keys_table.columns.id==item_id)
    result = await database.fetch_all(query)
    await database.execute(public_keys_table.delete().where(public_keys_table.columns.id==item_id))
    if not result :
        raise HTTPException(status_code=404,detail="Item not found",headers={"X-Error": "The item is missing or previously deleted"},)
    return templates.TemplateResponse("item2.html", {"request": request, "id": result[0][0] , "publickey" : result[0][1]})


@app.post("/addSecret/", response_model=SecretOut)
async def create_secret(secret: SecretIn):
    now_time = int(datetime.timestamp(datetime.now()))
    query = secrets.insert().values(ciphertext=secret.ciphertext, id=secret.id , timestamp=now_time) 
    last_record_id = await database.execute(query)
    return {**secret.dict(), "id": last_record_id}

@app.post("/addReceiverPK/", response_model=PublicKey)
async def create_publickey(pk: PublicKey):
    now_time = int(datetime.timestamp(datetime.now()))
    query = public_keys_table.insert().values(publickey=pk.publickey, id=pk.id , timestamp=now_time) 
    last_record_id = await database.execute(query)
    return {**pk.dict(), "id": last_record_id}

def repeat_every(*, seconds: float, wait_first: bool = False):
    def decorator(func: Callable[[], Optional[Awaitable[None]]]):
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def wrapped():
            async def loop():
                if wait_first:
                    await asyncio.sleep(seconds)
                while True:
                    try:
                        if is_coroutine:
                            await func()
                        else:
                            await run_in_threadpool(func)
                    except Exception as e:
                        #logger.error(str(e))
                        pass
                    await asyncio.sleep(seconds)

            asyncio.create_task(loop())

        return wrapped

    return decorator

async def delete_entry(table) :
    query = table.select()
    result = await database.fetch_all(query)
    if result :
        expired = list()
        now_time = int(datetime.timestamp(datetime.now()))
        for x in result :
            if now_time - x[2] > 60 * 60 * 24 :
                expired.append(x[0])
        for entry in expired :
            await database.execute(table.delete().where(table.columns.id==entry))


@app.on_event("startup")
@repeat_every(seconds=100)  # 24 hours
async def delete_old_entries():
    await delete_entry(secrets)
    await delete_entry(public_keys_table)
