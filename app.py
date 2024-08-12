from flask import Flask,render_template,request
import pandas as pd
import numpy as np
import joblib


app=Flask(__name__)

#load models and scalers
try:
    model  = joblib.load("cr_model.pkl")
    sc = joblib.load("RBScaler.pkl")
    print("\nModels and scaler loaded successfully\n")
except Exception as e:
    print(" An error occured: ", str(e))

@app.route("/")

def index():
    return render_template("index.html")

@app.route("/predict/",methods=['POST'])
def predict():

        N=float(request.form['Nitrogen'])
        P=float(request.form['Phosphorous'])
        K=float(request.form['Potassium'])
        temperature=float(request.form['Temperature'])
        humidity=float(request.form['Humidity'])
        ph=float(request.form['PH'])
        rainfall=float(request.form['Rainfall'])
        
        Dew_point = temperature- ((100- humidity)/5)
      
        
        feature = (np.array([N,P,K,temperature,humidity,ph,rainfall,Dew_point]).reshape(1,-1))
        
        scaled_feature = sc.transform(feature)
        
        pred = model.predict(scaled_feature)

        if float(humidity) >=1 and float(humidity)<= 33 : 
            humidity_level = 'Low Humid'
        elif float(humidity) >=34 and float(humidity) <= 66:
            humidity_level = 'Medium Humid'
        else:
            humidity_level = 'High Humid'

        if float(temperature) >= 0 and float(temperature)<= 6:
            temperature_level = 'Cool'
        elif float(temperature) >=7 and float(temperature):
            temperature_level = 'Warm'
        else:
            temperature_level= 'Hot' 

        if float(rainfall) >=1 and float(rainfall) <= 100:
            rainfall_level = 'Low'
        elif float(rainfall) >= 101 and float(rainfall) <=200:
            rainfall_level = 'Moderate'
        elif float(rainfall) >=201:
            rainfall_level = 'Heavy Rain'

        if float(N) >= 1 and float(N) <= 50: 
            N_level = 'Low'
        elif float(N) >=51 and float(N) <=100:
            N_level = 'Moderate'
        elif float(N) >=101:
            N_level = 'High'

        if float(P) >= 1 and float(P) <= 50:
            P_level = 'Low'
        elif float(P) >= 51 and float(P) <=100:
            P_level = 'Moderate'
        elif float(P) >=101:
            P_level = 'High'

        if float(K) >= 1 and float(K) <=50: 
            potassium_level = 'Low'
        elif float(K) >= 51 and float(K) <= 100:
            potassium_level = 'Moderate'
        elif float(K) >=101:
            potassium_level = 'High'

        if float(ph) >=0 and float(ph) <=5:             
            phlevel = 'Acidic' 
        elif float(ph) >= 6 and float(ph) <= 8:
            phlevel = 'Neutral'
        elif float(ph) >= 9 and float(ph) <= 14:
            phlevel = 'Alkaline'
        
        return render_template("Result.html",cont=[N_level,P_level,potassium_level,humidity_level,temperature_level,rainfall_level,phlevel],values=[N,P,K,humidity,temperature,rainfall,ph],cropName=pred)


if __name__=="__main__":
   app.run(debug=False)
  