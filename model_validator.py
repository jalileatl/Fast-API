from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Optional, Annotated, Dict

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient',
                               description='give name of the patient in 50 char',
                               example=['Nitish', 'Sandeep','Amit'])]
    email: EmailStr
    age: int = Field(gt=0, lt=120)
    linkdin: AnyUrl
    weight: float
    married: Optional[bool] = Field(default=None, description='Enter your marital status')
    allergies: List[str]
    contact_details: Dict[str, str]


    @model_validator(mode='after')
  

    def emergency_contact(cls, model):

        if model.age > 60 and not model.contact_details:
            raise ValueError("if patient age is greate than 60 then must have emergency contact details")
        
        return model


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
    print("updated ")

patient_info = {
    "name": "Nitish",
    "email": "abc@icici.com",
    "age": 90,
    "linkdin": "https://linkedin.com/in/abc",
    "weight": 56.50,
    "married": True,
    "allergies": ["skin allergies", "food allergies", "dust allergies"],
    'contact_details': {'contact': '9876543210', 'emergency_contact': '8765432109'}
}

patient1 = Patient(**patient_info)
insert_patient_info(patient1)

