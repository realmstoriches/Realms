\# FastAPI Overview



FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard type hints.



\## Core Features



\- \*\*Async support\*\*: Built on Starlette and Pydantic.

\- \*\*Automatic docs\*\*: Swagger and ReDoc out of the box.

\- \*\*Validation\*\*: Type-safe request and response models.



\## Example



```python

from fastapi import FastAPI



app = FastAPI()



@app.get("/ping")

def ping():

&nbsp;   return {"status": "alive"}

