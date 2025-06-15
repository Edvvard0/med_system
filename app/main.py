import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.config import settings
from app.patients.router import router as patient_router
from app.doctors.router import router as doctor_router
from app.hospitalization.router import router as hospitalization_router
from app.med_procedure.router import router as med_procedure_router
from app.pages.router import router as pages_router
from app.location.router import router as location_router


app = FastAPI()

app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(hospitalization_router)
app.include_router(med_procedure_router)
app.include_router(location_router)

app.include_router(pages_router)


app.mount("/static", StaticFiles(directory="app/static"), "static")


@app.get("/")
async def hello():
    return {"message": "hello"}


# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
