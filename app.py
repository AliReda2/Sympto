from flask import Flask, render_template, request, redirect, url_for, flash, session
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle
import json
import sqlite3

app = Flask(__name__)

symptom_list = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze', 'prognosis']
loaded_model = pickle.load(open('trained_model.sav','rb'))
label_encoder = pickle.load(open('label_encoder_target.sav','rb'))

file_path = 'disease_data.json'

# Open the file and load its content
with open(file_path, 'r') as file:
    disease_info = json.load(file)


@app.route('/')
def index():
    return render_template('ind.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        symptoms = request.form['symptoms']
        symptoms=symptoms.split(",")
        symptoms=[i.strip() for i in symptoms]
        input_vector = [0]*len(symptom_list)
        input_vector.pop()
        input_vector = np.array(input_vector)
        for i in symptoms:
            if i in symptom_list:
                input_vector[symptom_list.index(i)] = 1
        inp = input_vector.reshape(1,-1)

        probabilities = loaded_model.predict_proba(inp)

        top_n = 5
        top_classes = np.argsort(probabilities[0])[::-1][:top_n]  # Indices of the top N classes
        top_class_names = label_encoder.inverse_transform(top_classes)  # Convert indices back to class names
        top_probabilities = probabilities[0, top_classes]  # Probabilities of the top N classes
        possiblities = zip(top_class_names, top_probabilities)
        pred_info = []
        for i in top_class_names:
            pred_info.append(disease_info[i.strip()])
    
        return render_template('symptomOutput.html', prediction=possiblities, info = pred_info)
    
    return render_template('symptomInput.html')
        

@app.route('/output')
def predictions():
    return render_template('symptomOutput.html')

if __name__ == '__main__':
    app.run(debug=True)
