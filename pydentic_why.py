

from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Literal, Optional, Annotated

class Patient (BaseModel):
        name: Annotated [str, Field(max_length=50, title='Name of the patient', description='give name of the patient in 50 char',
                                    example=['Nitish', 'sandeep','amit'])]
        email:EmailStr
        age: int=Field(gt=0, lt=120)
        linkdin: AnyUrl
        weight: float
        married: Annotated[bool, Field(default=None, description='Enter your marital status')]
        allergies: List[str]
        contact_details: Optional[str] =None
        

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

patient_info={"name": 'Nitish', 'email':'abc@gmail.com', 'age': '90','linkdin':'https://linkdin.com/abc','weight':56.50, 'married':True, 'allergies': ['skin allergies', 'food allergies', 'dust allergies']}

patient1=Patient(**patient_info)


insert_patient_info(patient1)