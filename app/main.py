from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/homsqsqse")
def read_home():
    return {"Hello": "World"}
