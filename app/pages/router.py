from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.database import SessionDep
from app.doctors.dependencies import get_current_user, get_current_user_optional
from app.doctors.router import get_me_doc
from app.hospitalization.router import get_lst_hosp_full_info, get_patients_hosp
from app.med_procedure.router import (
    get_all_med_procedure,
    get_med_procedures,
    add_med_procedure,
    get_all_cabinets,
    get_all_med_procedure_by_current_patient,
    med_procedure_by_current_patient,
)
from app.patients.router import (
    get_me,
    get_patient,
    all_patients,
    get_all_hosp_by_patient_id,
)

router = APIRouter(prefix="/pages", tags=["Pages"])

template = Jinja2Templates(directory="app/templates")


@router.get("/")
async def info_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(name="index.html", context={"request": request})


@router.get("/login/patient")
async def login_patient_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(
        name="login.html", context={"request": request, "role": "patient"}
    )


@router.get("/patients/profile")
async def current_patient_page(
    request: Request, patient=Depends(get_me)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="patient_profile.html", context={"request": request, "patient": patient}
    )


@router.get("/patients")
async def patients_page(
    request: Request, patients=Depends(all_patients)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="lst_patients.html", context={"request": request, "patients": patients}
    )


@router.get("/patients/add")
async def patients_add_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(
        name="add_patient.html", context={"request": request}
    )


@router.get("/patients/{patient_id}")
async def current_patient_page(
    request: Request,
    doctor=Depends(get_current_user_optional),
    patient=Depends(get_patient),
) -> HTMLResponse:
    if doctor:
        role = "doctor"
    else:
        role = None

    return template.TemplateResponse(
        name="patient_profile.html",
        context={"request": request, "patient": patient, "role": role},
    )


@router.get("/login/doctor")
async def login_doctor_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(
        name="login.html", context={"request": request, "role": "doctor"}
    )


@router.get("/doctors/profile")
async def doctor_profile_page(
    request: Request, doctor=Depends(get_me_doc)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="main_doctor.html", context={"request": request, "doctor": doctor}
    )


@router.get("/doctors/{doctor_id}")
async def current_doctor_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse(
        name="login.html", context={"request": request, "role": "doctor"}
    )


@router.get("/hospitalizations")
async def hospitalizations_page(
    request: Request, lst_hosp=Depends(get_lst_hosp_full_info)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="lst_hosp.html", context={"request": request, "hospitalizations": lst_hosp}
    )


@router.get("/hospitalizations/patient/{patient_id}")
async def hospitalizations_current_patient_page(
    request: Request, patient=Depends(get_all_hosp_by_patient_id)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="lst_hosp.html",
        context={"request": request, "hospitalizations": patient.hospitalizations},
    )


@router.get("/hospitalizations/add/{patient_id}")
async def add_hospitalizations_page(
    request: Request,
    patient_id: int,
) -> HTMLResponse:
    return template.TemplateResponse(
        name="add_hospitalizations.html", context={"request": request}
    )


@router.get("/hospitalizations/{hosp_id}")
async def hospitalizations_page(
    request: Request, hosp=Depends(get_patients_hosp)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="current_hosp.html", context={"request": request, "hospitalization": hosp}
    )


@router.get("/med_procedures")
async def med_procedures_page(
    request: Request, med_procedures=Depends(get_all_med_procedure)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="lst_med_procedure.html",
        context={"request": request, "med_procedures": med_procedures},
    )


@router.get("/med_procedures/patient/{patient_id}")
async def med_procedures_current_patient_page(
    request: Request, med_procedure=Depends(get_all_med_procedure_by_current_patient)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="lst_med_procedure.html",
        context={"request": request, "med_procedures": med_procedure},
    )


@router.get("/med_procedures/add/{patient_id}")
async def med_procedures_page(
    request: Request, patient_id: int, cabinets=Depends(get_all_cabinets)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="add_med_procedure.html",
        context={"request": request, "cabinets": cabinets},
    )


@router.get("/med_procedures/{med_procedures_id}")
async def med_procedures_page(
    request: Request, med_procedure=Depends(get_med_procedures)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="current_med_procedure.html",
        context={"request": request, "med_procedure": med_procedure},
    )


@router.get("/graph")
async def graph_page(
    request: Request, med_procedure=Depends(med_procedure_by_current_patient)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="graph.html", context={"request": request, "med_procedures": med_procedure}
    )
