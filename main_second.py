from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json, os

app = FastAPI(title="Patient Management API")


# -----------------------------
# Patient Model
# -----------------------------
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Unique ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City of the patient")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[
        Literal["male", "female", "others"],
        Field(..., description="Gender of the patient", example="male"),
    ]
    height: Annotated[float, Field(..., description="Height of the patient in meters")]
    weight: Annotated[float, Field(..., description="Weight of the patient in kg")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height**2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "normal_weight"
        elif 25 <= self.bmi < 29.9:
            return "overweight"
        else:
            return "obese"


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    city: Annotated[Optional[str], Field(default=None)]
    gender: Annotated[
        Optional[Literal["Male", "Female"]],
        Field(default=None, description="Gender of the patient"),
    ]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]         

# -----------------------------
# Utility functions
# -----------------------------
def load_data():
    if not os.path.exists("patient.json"):
        return {}
    try:
        with open("patient.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_data(data):
    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def hello():
    return {"Message": "Patient Management API"}


@app.get("/jalil")
def hi():
    return {"Name": "A fully functional API for patient management"}


@app.get("/view")
def view():
    return load_data()


@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient in DB", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="File not found")


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight and bmi"),
    order: str = Query("asc", description="Sort by asc or desc order"),
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Choose from {valid_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Use asc or desc")

    data = load_data()
    sort_order = order == "desc"
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    data[patient.id] = patient.model_dump()
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})


@app.put("edit/{patient_id}")

def update_patient(patient_id: str, patient_update: PatientUpdate):

    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")
    
    existing_patient_info=data[patient_id]

    updated_patient_info=patient_update.model_dump(exclude_onset=True)

    for key, value in updated_patient_info.items():

        existing_patient_info[key]=value

    existing_patient_info[id]=patient_id


    patient_pydantic_obj=Patient(**existing_patient_info)



        #existing_patient_info -> pydantic object -> updated bmi+verdict
        #pydantic object -> dict

    existing_patient_info=patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id]=existing_patient_info

    save_data(data)
 
