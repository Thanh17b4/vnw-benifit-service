import uvicorn
from fastapi import FastAPI
from benefit import benefit_router

app = FastAPI()

app.include_router(benefit_router)
uvicorn.run(app, host="localhost", port=5004)
