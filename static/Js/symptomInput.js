var symptom_list = [
    'Itching', 'Skin Rash', 'Nodal Skin Eruptions', 'Continuous Sneezing', 'Shivering', 'Chills', 'Joint Pain', 'Stomach Pain',
    'Acidity', 'Ulcers On Tongue', 'Muscle Wasting', 'Vomiting', 'Burning Micturition', 'Spotting Urination', 'Fatigue',
    'Weight Gain', 'Anxiety', 'Cold Hands And Feets', 'Mood Swings', 'Weight Loss', 'Restlessness', 'Lethargy',
    'Patches In Throat', 'Irregular Sugar Level', 'Cough', 'High Fever', 'Sunken Eyes', 'Breathlessness', 'Sweating',
    'Dehydration', 'Indigestion', 'Headache', 'Yellowish Skin', 'Dark Urine', 'Nausea', 'Loss Of Appetite', 'Pain Behind The Eyes',
    'Back Pain', 'Constipation', 'Abdominal Pain', 'Diarrhoea', 'Mild Fever', 'Yellow Urine', 'Yellowing Of Eyes',
    'Acute Liver Failure', 'Fluid Overload', 'Swelling Of Stomach', 'Swelled Lymph Nodes', 'Malaise', 'Blurred And Distorted Vision',
    'Phlegm', 'Throat Irritation', 'Redness Of Eyes', 'Sinus Pressure', 'Runny Nose', 'Congestion', 'Chest Pain', 'Weakness In Limbs',
    'Fast Heart Rate', 'Pain During Bowel Movements', 'Pain In Anal Region', 'Bloody Stool', 'Irritation In Anus', 'Neck Pain',
    'Dizziness', 'Cramps', 'Bruising', 'Obesity', 'Swollen Legs', 'Swollen Blood Vessels', 'Puffy Face And Eyes', 'Enlarged Thyroid',
    'Brittle Nails', 'Swollen Extremeties', 'Excessive Hunger', 'Extra Marital Contacts', 'Drying And Tingling Lips', 'Slurred Speech',
    'Knee Pain', 'Hip Joint Pain', 'Muscle Weakness', 'Stiff Neck', 'Swelling Joints', 'Movement Stiffness', 'Spinning Movements',
    'Loss Of Balance', 'Unsteadiness', 'Weakness Of One Body Side', 'Loss Of Smell', 'Bladder Discomfort', 'Foul Smell Of Urine',
    'Continuous Feel Of Urine', 'Passage Of Gases', 'Internal Itching', 'Toxic Look (Typhos)', 'Depression', 'Irritability',
    'Muscle Pain', 'Altered Sensorium', 'Red Spots Over Body', 'Belly Pain', 'Abnormal Menstruation', 'Dischromic Patches',
    'Watering From Eyes', 'Increased Appetite', 'Polyuria', 'Family History', 'Mucoid Sputum', 'Rusty Sputum', 'Lack Of Concentration',
    'Visual Disturbances', 'Receiving Blood Transfusion', 'Receiving Unsterile Injections', 'Coma', 'Stomach Bleeding',
    'Distention Of Abdomen', 'History Of Alcohol Consumption', 'Fluid Overload', 'Blood In Sputum', 'Prominent Veins On Calf',
    'Palpitations', 'Painful Walking', 'Pus Filled Pimples', 'Blackheads', 'Scurring', 'Skin Peeling', 'Silver Like Dusting',
    'Small Dents In Nails', 'Inflammatory Nails', 'Blister', 'Red Sore Around Nose', 'Yellow Crust Ooze', 'Prognosis'
  ];
  
  function filterSuggestions() {
    var symptomsInput = document.getElementById('symptomsInput');
    var suggestionsList = document.getElementById('suggestions');
    suggestionsList.innerHTML = '';  // Clear previous suggestions
  
    // Filter allowed values based on user input
    var filteredValues = symptom_list.filter(function (value) {
      return value.toLowerCase().includes(symptomsInput.value.toLowerCase());
    });
  
    // Display filtered suggestions
    filteredValues.forEach(function (value) {
      var listItem = document.createElement('li');
      listItem.textContent = value;
      listItem.onclick = function () {
        addToSelectedItems(value);
      };
      suggestionsList.appendChild(listItem);
    });
  }
  
  function addToSelectedItems(value) {
    var selectedItemsList = document.getElementById('itemList');
  
    // Check if the value is already in the list
    if (!isSymptomAlreadySelected(value)) {
      var listItem = document.createElement('li');
      listItem.textContent = value;
      selectedItemsList.appendChild(listItem);
  
      // Clear the input field after selecting an item
      document.getElementById('symptomsInput').value = '';
  
      // Update the string (comma-separated values)
      updateString();
    } else {
      alert('Symptom already selected.');
    }
    document.getElementById('suggestions').style.display = "none";
  }
  
  function isSymptomAlreadySelected(value) {
    var selectedItemsList = document.getElementById('itemList');
    var items = selectedItemsList.getElementsByTagName('li');
  
    // Check if the value is already in the list
    for (var i = 0; i < items.length; i++) {
      if (items[i].textContent.toLowerCase() === value.toLowerCase()) {
        return true; // Symptom already selected
      }
    }
  
    return false; // Symptom not selected
  }
  
  let selectedString = "";
  
  function updateString() {
    var selectedItemsList = document.getElementById('itemList');
    var items = selectedItemsList.getElementsByTagName('li');
    var selectedValues = [];
  
    // Extract selected values
    for (var i = 0; i < items.length; i++) {
      selectedValues.push(items[i].textContent);
    }
  
    // Join the selected values into a comma-separated string
    selectedString = selectedValues.join(', ');
  
    // Update the value of the hidden form field
    document.getElementById('hiddenSelectedString').value = selectedString;
  
    // Display the resulting string (you can use it when the user submits)
    console.log(selectedString);
  }
  
  function showSuggestions() {
    document.getElementById('suggested').style.display = "block";
    document.getElementById('suggestions').style.display = "block";
  }
  
  document.getElementById('symptomsInput').addEventListener('input', showSuggestions);
  