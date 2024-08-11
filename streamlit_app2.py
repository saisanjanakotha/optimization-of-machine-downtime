# -*- coding: utf-8 -*-
"""
Created on Tue May 14 12:14:32 2024

@author: SAI SANJANA.KOTHA
"""
#pip install streamlit
import pandas as pd
import streamlit as st 
# import numpy as np

#pip install joblib
#pip install pickle
import pickle, joblib

model = joblib.load('decision_tree_model.joblib')
impute = joblib.load('imp_enc_scale')
winsor = joblib.load('winsor')


def predict_Downtime(data):

   
    data = data.drop(columns=['Date'])
    st.write(data)
    clean = pd.DataFrame(impute.transform(data), columns=impute.get_feature_names_out())
    clean[['num__Hydraulic_Pressure(bar)', 'num__Coolant_Pressure(bar)',
           'num__Air_System_Pressure(bar)', 'num__Coolant_Temperature',
           'num__Hydraulic_Oil_Temperature(°C)',
           'num__Spindle_Bearing_Temperature(°C)', 'num__Spindle_Vibration(µm)',
           'num__Tool_Vibration(µm)', 'num__Spindle_Speed(RPM)',
           'num__Voltage(volts)', 'num__Torque(Nm)', 'num__Cutting(kN)']] = winsor.transform(clean[['num__Hydraulic_Pressure(bar)', 'num__Coolant_Pressure(bar)',
           'num__Air_System_Pressure(bar)', 'num__Coolant_Temperature',
           'num__Hydraulic_Oil_Temperature(°C)',
           'num__Spindle_Bearing_Temperature(°C)', 'num__Spindle_Vibration(µm)',
           'num__Tool_Vibration(µm)', 'num__Spindle_Speed(RPM)',
           'num__Voltage(volts)', 'num__Torque(Nm)', 'num__Cutting(kN)']])

    prediction = pd.DataFrame(model.predict(clean), columns = ['prediction'])
    
    # Replace 0 and 1 with "No Downtime" and "Downtime" respectively
    prediction['prediction'] = prediction['prediction'].replace({0: 'No Downtime', 1: 'Downtime'})
    
    final = pd.concat([prediction,data], axis = 1)
    ##final.to_sql('Downtime_predictons', con = engine, if_exists = 'replace', chunksize = 1000, index = False)

    return final



def main():
    

    st.title("Optimization of Machine Downtime")
    st.sidebar.title("Optimization of Machine Downtime")

    # st.radio('Type of Cab you want to Book', options=['Mini', 'Sedan', 'XL', 'Premium', 'Rental'])
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Optimization of Machine Downtime App </h2>
    </div>
    
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    st.text("")
    

    uploadedFile = st.sidebar.file_uploader("Choose a file", type=['csv','xlsx'], accept_multiple_files=False, key="fileUploader")
    if uploadedFile is not None :
        try:

            data = pd.read_csv(uploadedFile)
        except:
                try:
                    data = pd.read_excel(uploadedFile)
                except:      
                    data = pd.DataFrame()
        
        
    else:
        st.sidebar.warning("You need to upload a CSV or an Excel file.")
    
    # html_temp = """
    # <div style="background-color:tomato;padding:10px">
    # <p style="color:white;text-align:center;">Add DataBase Credientials </p>
    # </div>
    # """
    # st.sidebar.markdown(html_temp, unsafe_allow_html = True)
            
    # user = st.sidebar.text_input("user", "Type Here")
    # pw = st.sidebar.text_input("password", "Type Here")
    # db = st.sidebar.text_input("database", "Type Here")
    
  
    if st.button("Predict"):
        result = predict_Downtime(data)
        #st.dataframe(result) or
        #st.table(result.style.set_properties(**{'background-color': 'white','color': 'black'}))
                           
        import seaborn as sns
        cm = sns.light_palette("blue", as_cmap = True)
        st.table(result)

if __name__=='__main__':
    main()


