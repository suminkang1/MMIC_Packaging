import tensorflow as tf
from tensorflow import keras
import pandas as pd
from PIL import Image
import streamlit as st

Learning_Model = keras.models.load_model('ANN_128_128_128_128_128')


#Create a title
st.write("""
## Thermo-mechanical analysis of MMIC packaging
""")

#Open and display an image
GaN_MMIC_image = Image.open('MMIC_Packaging_2.PNG')
st.image(GaN_MMIC_image, use_column_width=True, clamp=True)

#Get the feature input from the user
st.sidebar.header('Design parameters')
def get_user_input():
    k_Adhe = st.sidebar.number_input('Thermal conductivity of adhesive (W/mK)', 50.00, 200.00, 57.00)
    CTE_Adhe = st.sidebar.number_input('CTE of adhesive (ppm/K)', 15.00, 25.00, 20.00)
    E_Adhe = st.sidebar.number_input('Elastic modulus of adhesive (GPa)', 20.00, 80.00, 40.00)
    v_Adhe = st.sidebar.number_input('Poisson ratio of adhesive', 0.350, 0.400, 0.370)
    k_Carr = st.sidebar.number_input('Thermal conductivity of carrier (W/mK)', 150.00, 450.00, 200.00)
    CTE_Carr = st.sidebar.number_input('CTE of carrier (ppm/K)', 5.00, 23.00, 11.00)
    E_Carr = st.sidebar.number_input('Elastic modulus of carrier (GPa)', 50.00, 350.00, 200.00)
    v_Carr = st.sidebar.number_input('Poisson ratio of carrier', 0.250, 0.350, 0.300)
    T_Chip = st.sidebar.number_input('Chip thickness (um)', 30.00, 200.00, 100.00)
    T_Adhe = st.sidebar.number_input('Adhesive thickness (um)', 10.00, 100.00, 30.00)
    T_Carr = st.sidebar.number_input('Carrier thickness (mm)', 0.300, 2.500, 1.000)
    Flux = st.sidebar.number_input('Heat flux (W/mK)', 1.00, 30.00, 5.55)
    Conv = st.sidebar.number_input('Heat transfer coefficient (W/m2K)', 0.00, 300.00, 100.00)

    
    #Store a dictionary into a variable
    user_data = {'k_Adhe':k_Adhe, 
                     'CTE_Adhe':CTE_Adhe,
                     'E_Adhe':E_Adhe, 
                     'v_Adhe':v_Adhe,
                     'k_Carr':k_Carr,
                     'CTE_Carr':CTE_Carr, 
                     'E_Carr':E_Carr, 
                     'v_Carr':v_Carr,
                     'Flux':Flux,
                     'Conv':Conv,    
                     'T_Chip':T_Chip, 
                     'T_Adhe':T_Adhe,
                     'T_Carr':T_Carr}
    
    #Transform the data into a data frame
    features = pd.DataFrame(user_data, index = [0])
    return features

#Store the user input into a variable
user_input = get_user_input()

Prediction = Learning_Model.predict(user_input)
Temp = pd.Series(Prediction.T[0])
S_Chip = pd.Series(Prediction.T[1])
S_Adhe = pd.Series(Prediction.T[2])

Final_Temp = str(round(Temp[0], 3))
Final_S_Chip = str(round(S_Chip[0], 3))
Final_S_Adhe = str(round(S_Adhe[0], 3))

#Display the result
st.write("#####")
st.write("### Analysis results")
st.write("#####")
st.write("##### Maximum temperature = {} ℃".format(Final_Temp))
st.write("#####")
st.write("##### Maximum principal stress in chip = {} MPa".format(Final_S_Chip))
st.write("#####")
st.write("##### Maximum mises stress in adhesive = {} MPa".format(Final_S_Adhe))
