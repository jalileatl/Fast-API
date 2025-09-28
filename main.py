from fastapi import FastAPI, Path, HTTPException, Query
import json

app=FastAPI()

def load_data():
    with open("patients.json","r") as f:
        data= json.load(f)

    return data
        

@app.get("/")

def hello ():
    
    return {"Message": "Patient Management API"}

@app.get("/jalil")

def hi():
        
 return {"Name":  "A fully functional API for patient management"}


@app.get("/view")

def view():
   
   data=load_data()

   return data

@app.get("/patient/{patient_id}")

def view_patient(patient_id: str = Path(..., description='The path of the patient in DB', example='P001')):
   
   data=load_data()

   if patient_id in data:
      return data[patient_id]
   
   raise HTTPException(status_code=404, description='File not found')


@app.get('/sort')

def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight and bmi"), 
                  order: str= Query('asc', description='sort by asc order')):
     
                        valid_fields=['height', 'weight', 'bmi']
                        
                        if sort_by not in valid_fields:
                    
                         raise HTTPException (status_code=400, detail='Invalid fields selected from {valid_fields}')
                        
                        if order not in ['asc', 'desc']:
                             
                            raise HTTPException (status_code=400, detail='Invalid code selected from asc and desc')
                        
                        data=load_data()

                        sort_order=True if order=='desc' else False

                        sorted_data=sorted(data.values(), key=lambda x:x.get(sort_by, 0), reverse=sort_order)

                        return sorted_data


                        


   



   