# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


if __name__ == '__main__':
    uvicorn.run(app='main:app',port=8888)

