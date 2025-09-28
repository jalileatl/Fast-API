from pydantic import BaseModel, EmailStr, AnyUrl, computed_field, Field
from typing import List, Optional, Annotated, Dict

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int 
    linkdin: AnyUrl
    weight: float
    height: float
    married: Optional[bool] = None
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi=round(self.weight / (self.height ** 2),2)

        return bmi
    
     






    


def insert_patient_info(patient: Patient):
    print("name of patient: ", patient.name)
    print("age of patient: ", patient.age)
    print('Linkdin url: ', patient.linkdin)
    print('Email of patient: ', patient.email)
    print("weight of patient: ", patient.weight)
    print("married of patient: ", patient.married)
    print("allergies of patient: ", patient.allergies)
    print('Contact details: ', patient.contact_details)
    print("Inserted! ")

def update_patient_info(patient: Patient):
    print("name of patient: ", patient.name)
    print("age of patient: ", patient.age)
    print("bmi of patient: ", patient.calculate_bmi)
    print("updated ")

patient_info = {
    "name": "Nitish",
    "email": "abc@icici.com",
    "age": 90,
    "linkdin": "https://linkedin.com/in/abc",
    "weight": 64,
    "height": 1.71,
    "married": True,
    "allergies": ["skin allergies", "food allergies", "dust allergies"],
    'contact_details': {'contact': '9876543210', 'emergency_contact': '8765432109'}
}

patient1 = Patient(**patient_info)
update_patient_info(patient1)

