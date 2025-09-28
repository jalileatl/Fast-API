from pydantic import BaseModel


class Address(BaseModel):
    stree: str
    city: str
    house_no: int


class Patient(BaseModel):
    name: str
    age:int
    address: Address


address_dict={"stree": "MG Road",
              "city": "Bangalore",
              "house_no": 12}

address1=Address(**address_dict)

patient_dict={"name": "Nitihs", 'age': 30, 'address': address1}


patient1=Patient(**patient_dict)

print(patient1)
print(patient1.address.city)