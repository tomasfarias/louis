import os
import secrets
import typing

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

from louis.nest import process_json_array

app = FastAPI()
security = HTTPBasic()


def check_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, os.getenv("LOUIS_USERNAME")
    )
    correct_password = secrets.compare_digest(
        credentials.password, os.getenv("LOUIS_PASSWORD")
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/health")
async def health(credentials: HTTPBasicCredentials = Depends(check_credentials)):
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "10-4 all systems green"}
    )


class NestMe(BaseModel):
    json_array: typing.List[typing.Dict[typing.Any, typing.Any]]
    keys: typing.List[str]


@app.post("/nestme")
async def nest_me(
    nest_me: NestMe, credentials: HTTPBasicCredentials = Depends(check_credentials)
):
    nested = process_json_array(nest_me.json_array, *nest_me.keys)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=nested,
    )
