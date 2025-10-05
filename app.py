from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd
from fastapi.response import JSONResponse

with open('model.pkl', 'rb') as f:
    model= pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the user')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user')]
    height: Annotated [float, Field(..., gt=0, lt=2.5, description='height of the user in  cm')]
    income_lpa: Annotated [float, Field(..., gt=0, description='Income of the user')]
    smoker: Annotated [bool, Field(..., description='is user smoker')]
    city: Annotated [str, Field(..., description='The city the user belongs to')]

    occupaton: Annotated [Literal['retired', 'freelancer', 'student', 'goverment_job' ,'business_owner', 'unemployed', 'private_job'], Field(..., gt=0, lt=120, description='Occupaton of the user')]

    @computed_field
    @property
    def bmi (self) -> float:
        height_in_m = self.height /100
        return self.weight / (height_in_m ** 2)
    
    @computed_field
    @property
    def lifestyle_risk (self) -> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 27:
            return 'medium'
        return 'low'
    
    @computed_field
    @property
    def age_group(self) -> str:

        if self.age < 18:
            return 'child'
        elif 18 <= self.age < 35:
            return 'adult'
        elif 35 <= self.age < 60:

            return 'middle_aged'
        return 'senior'
    
    @computed_field
    @property
    def city_tier (self) -> str:
        if self.city in tier_1_cities:
            return 'tier_1'
        elif self.city in tier_2_cities:
            return 'tier_2'
        return 'tier_3'
    


@app.post('/predict')

def predict_premium (data: UserInput):
    
    input_df=pd.DataFrame ([
        {
            'bmi': data.bmi,
            'age_group': data.age_group,
            'lifestyle_risk': data.lifestyle_risk,
            'city_tier': data.city_tier,
            'income_lpa': data.income_lpa,
            'occupation': data.occupation
        }
    ])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'prediction_category': prediction} )


    
    
