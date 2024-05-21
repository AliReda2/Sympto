"""
If running on the local machine, remove all multiline comment

Few features can't work on hosted website via Github CI/CD due to pricing issues
"""
from flask import Flask, render_template, request, url_for, redirect
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle
import json
# """
# import pandas as pd
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords
# import nltk
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.svm import SVC
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# """
app = Flask(__name__)

symptom_list = ['Itching', 'Skin Rash', 'Nodal Skin Eruptions', 'Continuous Sneezing', 'Shivering', 'Chills', 'Joint Pain', 'Stomach Pain', 'Acidity', 'Ulcers On Tongue', 'Muscle Wasting', 'Vomiting', 'Burning Micturition', 'Spotting Urination', 'Fatigue', 'Weight Gain', 'Anxiety', 'Cold Hands And Feets', 'Mood Swings', 'Weight Loss', 'Restlessness', 'Lethargy', 'Patches In Throat', 'Irregular Sugar Level', 'Cough', 'High Fever', 'Sunken Eyes', 'Breathlessness', 'Sweating', 'Dehydration', 'Indigestion', 'Headache', 'Yellowish Skin', 'Dark Urine', 'Nausea', 'Loss Of Appetite', 'Pain Behind The Eyes', 'Back Pain', 'Constipation', 'Abdominal Pain', 'Diarrhoea', 'Mild Fever', 'Yellow Urine', 'Yellowing Of Eyes', 'Acute Liver Failure', 'Fluid Overload', 'Swelling Of Stomach', 'Swelled Lymph Nodes', 'Malaise', 'Blurred And Distorted Vision', 'Phlegm', 'Throat Irritation', 'Redness Of Eyes', 'Sinus Pressure', 'Runny Nose', 'Congestion', 'Chest Pain', 'Weakness In Limbs', 'Fast Heart Rate', 'Pain During Bowel Movements', 'Pain In Anal Region', 'Bloody Stool', 'Irritation In Anus', 'Neck Pain', 'Dizziness', 'Cramps', 'Bruising', 'Obesity', 'Swollen Legs', 'Swollen Blood Vessels', 'Puffy Face And Eyes', 'Enlarged Thyroid', 'Brittle Nails', 'Swollen Extremeties', 'Excessive Hunger', 'Extra Marital Contacts', 'Drying And Tingling Lips', 'Slurred Speech', 'Knee Pain', 'Hip Joint Pain', 'Muscle Weakness', 'Stiff Neck', 'Swelling Joints', 'Movement Stiffness', 'Spinning Movements', 'Loss Of Balance', 'Unsteadiness', 'Weakness Of One Body Side', 'Loss Of Smell', 'Bladder Discomfort', 'Foul Smell Of Urine', 'Continuous Feel Of Urine', 'Passage Of Gases', 'Internal Itching', 'Toxic Look (Typhos)', 'Depression', 'Irritability', 'Muscle Pain', 'Altered Sensorium', 'Red Spots Over Body', 'Belly Pain', 'Abnormal Menstruation', 'Dischromic Patches', 'Watering From Eyes', 'Increased Appetite', 'Polyuria', 'Family History', 'Mucoid Sputum', 'Rusty Sputum', 'Lack Of Concentration', 'Visual Disturbances', 'Receiving Blood Transfusion', 'Receiving Unsterile Injections', 'Coma', 'Stomach Bleeding', 'Distention Of Abdomen', 'History Of Alcohol Consumption', 'Fluid Overload', 'Blood In Sputum', 'Prominent Veins On Calf', 'Palpitations', 'Painful Walking', 'Pus Filled Pimples', 'Blackheads', 'Scurring', 'Skin Peeling', 'Silver Like Dusting', 'Small Dents In Nails', 'Inflammatory Nails', 'Blister', 'Red Sore Around Nose', 'Yellow Crust Ooze', 'Prognosis']

sympto_model = pickle.load(open('Model_Files/trained_model.sav','rb'))
label_encoder = pickle.load(open('Model_Files/label_encoder_target.sav','rb'))

vectorizer = pickle.load(open('Model_Files/Vectorizer.sav','rb'))

data_file_path = 'Model_Files/data.csv'
file_path = 'Model_Files/disease_data.json'

with open(file_path, 'r') as file:
    disease_info = json.load(file)
# """
# def remove_stopwords(text):
#     stpw=set(stopwords.words('english'))
#     filtered_text=[word for word in text if word not in stpw]
#     return filtered_text

# def lemmatize_words(text):
#     lemmer=WordNetLemmatizer()
#     lemmatized_text=[lemmer.lemmatize(word,pos='v') for word in text]
#     return lemmatized_text
# """
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        age = request.form['age']
        sex = request.form['sex']

        # Vercel has a Read-Only Filesystem, so we can't write to the file currently hosted
        # on Vercel. Uncomment the following code to write to a local file
        
        with open(data_file_path, mode='a', newline='') as csvfile:
            fieldnames = ['Age', 'Sex']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'Age': age, 'Sex': sex})
        
        return redirect(url_for('predict'))
    return render_template('ind.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        symptoms = request.form['selectedString'][2:]
        print(symptoms)
        symptoms=symptoms.split(",")
        symptoms=[i.strip() for i in symptoms]
        
        input_vector = [0]*len(symptom_list)
        input_vector.pop()
        input_vector = np.array(input_vector)
        for i in symptoms:
            if i in symptom_list:
                input_vector[symptom_list.index(i)] = 1
        inp = input_vector.reshape(1,-1)

        probabilities = sympto_model.predict_proba(inp)

        top_n = 5
        top_classes = np.argsort(probabilities[0])[::-1][:top_n]  # Indices of the top N classes
        top_class_names = label_encoder.inverse_transform(top_classes)  # Convert indices back to class names
        top_probabilities = probabilities[0, top_classes]  # Probabilities of the top N classes
        top_probabilities = [f"{int(i*100)}" for i in top_probabilities]
        possiblities = zip(top_class_names, top_probabilities)

        pred_info = []
        for i in top_class_names:
            pred_info.append(disease_info[i.strip()])
    
        return render_template('symptomOutput.html', prediction=list(possiblities), info = pred_info)
    
    return render_template('symptomInput.html')

@app.route('/mental', methods=['GET', 'POST'])
def mental():
    if request.method == "POST":
        # """
        # input = request.form['feelings']
        # input=pd.DataFrame({
        #     'text':[input]
        # })
        # input['text']=input['text'].apply(word_tokenize)
        # input['text']=input['text'].apply(remove_stopwords)
        # input['text']=input['text'].apply(lemmatize_words)
        # input['text']=input['text'].apply(lambda x : ' '.join([index for index in x]))
        # X_valid=vectorizer.transform(input['text'])
        # stress_output=mental_model.predict(X_valid)
        # stress_probab = mental_model.predict_proba(X_valid)[0][1]
        # if stress_output==0:
        #     stress_output='Not Stress'
        # else:
        #     stress_output='Stress'
        
        # return render_template('mentalhealthoutput.html', output=stress_output)
        # """
        return render_template('mentalhealth.html',msg="Cant host")
        
    return render_template('mentalhealth.html')

@app.route('/output')
def predictions():
    return render_template('symptomOutput.html')

if __name__ == '__main__':
    app.run(debug=True)
