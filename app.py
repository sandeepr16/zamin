from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('croptype1.sav', 'rb'))
model2 = pickle.load(open('fertilizer1.sav','rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        number=int(request.form['number'])
        o = list(map(int, str(number)))
        temp= int(str(o[0])+str(o[1]))
        humid= int(str(o[2])+str(o[3]))
        moist= int(str(o[4])+str(o[5]))
        soiltype= int(o[6])
        nitro= int(str(o[7])+str(o[8]))
        potas= int(str(o[9])+str(o[10]))
        phos= int(str(o[11])+str(o[12]))
        fv=[temp,humid,moist,soiltype,nitro,potas,phos]
        fv = np.array(fv).reshape((1,-1))
        prediction=model.predict(fv)
        crop =  { 'Maize':1, 'Sugarcane':2, 'Cotton':3 ,'Tobacco':4, 'Paddy':5, 'Barley':6,'Wheat':7, 'Millets':8, 'Oil seeds':9, 'Pulses':10, 'Ground Nuts':11 }
        crop_name=list(crop.keys())[list(crop.values()).index(prediction)]
        prediction1=model2.predict([[temp,humid,moist,soiltype,prediction,nitro,potas,phos]])
        fert_name = {'Urea': 1,'DAP': 2,'14-35-14':3, '28-28':4, '17-17-17':5, '20-20':6,'10-26-26':7}
        y=list(fert_name.keys())[list(fert_name.values()).index(prediction1)]


        return render_template('index.html',prediction_text="Crop Name:{} Fertilizer Comp :{}".format(crop_name,y))
        
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

