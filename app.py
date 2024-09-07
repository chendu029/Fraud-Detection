from flask import Flask, render_template, request
import pickle
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load the saved model
model = pickle.load(open('fraud_detection__2.pkl', 'rb'))

# Define the homepage route
@app.route('/')
def index():
    return render_template('index.html')

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    step = request.form.get('step', type=int)
    type_ = request.form.get('type')
    amount = request.form.get('amount', type=float)
    oldbalanceOrg = request.form.get('oldbalanceOrg', type=float)
    newbalanceOrig = request.form.get('newbalanceOrig', type=float)
    oldbalanceDest = request.form.get('oldbalanceDest', type=float)
    newbalanceDest = request.form.get('newbalanceDest', type=float)

    # Create DataFrame for prediction
    input_data = pd.DataFrame({
        'step': [step],
        'type': [type_],
        'amount': [amount],
        'oldbalanceOrg': [oldbalanceOrg],
        'newbalanceOrig': [newbalanceOrig],
        'oldbalanceDest': [oldbalanceDest],
        'newbalanceDest': [newbalanceDest]
    })

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Display the result
    result = "This transaction is likely fraudulent." if prediction == 1 else "This transaction is likely NOT fraudulent."

    return render_template('index.html', prediction_text=result)

if __name__ == "__main__":
    app.run(debug=True)
