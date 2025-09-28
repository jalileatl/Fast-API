from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Optional, Annotated

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
    contact_details: Optional[str] = None

    @field_validator("email", mode='after')
    @classmethod
    def email_validator(cls, value):
        valid_domain = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domain:
            raise ValueError('Not a valid email')
        return value

    @field_validator("name", mode='before')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator("age", mode='after')

    @classmethod

    def validate_age(cls, value):
        if 0<value<120:
            return value
        else:
            raise ValueError("Age must be between 1 and 59")

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
    "allergies": ["skin allergies", "food allergies", "dust allergies"]
}

patient1 = Patient(**patient_info)
insert_patient_info(patient1)
