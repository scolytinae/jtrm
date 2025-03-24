from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/template/{template_name}")
def read_template(template_name: str, q: Union[str, None] = None):
    return {"template_name": template_name, "q": q}

