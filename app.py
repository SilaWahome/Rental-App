import os
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

#definition Tax and relief constants
PERSONAL_RELIEF = 2400
SHIF_RATE = 0.01

#PAYE calculation function based on the Kenya tax bands
def calculate_paye(income):
    paye = 0
    if income <= 24000:
        paye = income * 0.10
    elif income <= 24000 + 8333:
        paye = (24000 * 0.10) + (income - 24000) * 0.25
    elif income <= 24000 + 8333 + 467667:
        paye = (24000 * 0.10) + (8333 * 0.25) + (income - 24000 - 8333) * 0.30
    elif income <= 800000:
        paye = (24000 * 0.10) + (8333 * 0.25) + (467667 * 0.30) + (income - 24000 - 8333 - 467667) * 0.325
    else:
        paye = (24000 * 0.10) + (8333 * 0.25) + (467667 * 0.30) + (300000 * 0.325) + (income - 800000) * 0.35
    return max(paye, 0)

# Function to calculate net income (Gross Income - PAYE - SHIF + Personal Relief)
def calculate_net_income(gross_income):
    paye = calculate_paye(gross_income)
    shif = gross_income * SHIF_RATE
    return gross_income - paye - shif + PERSONAL_RELIEF

# Function to filter suitable places based on user's net income and preferences
def suggest_places(df, net_income):
    # Maximum rent is the lesser of 30% of net income and net income
    max_rent = min(0.30 * net_income, net_income)
    
    # Filter based on rent
    suitable_places = df[df['Price'] <= max_rent]
    
    # If no listings available, return None
    if suitable_places.empty:
        return None
    
    # Randomly select up to 2 places
    num_places = min(2, len(suitable_places))
    selected_places = suitable_places.sample(n=num_places, replace=False)
    
    # Select only the desired columns for output
    result = selected_places[['Agency', 'Neighborhood', 'Price', 'Bedrooms']]
    return result

# Route to load the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to process form data
@app.route('/result', methods=['POST'])
def result():
    gross_income = float(request.form['gross_income'])
    csv_path = os.path.join(os.path.dirname(__file__), 'rent_apts.csv')
    df = pd.read_csv(csv_path)

    # Clean and convert data types
    df['Agency'] = df['Agency'].astype(str)
    df['Neighborhood'] = df['Neighborhood'].astype(str)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Bedrooms'] = pd.to_numeric(df['Bedrooms'], errors='coerce')
    df['Bathrooms'] = pd.to_numeric(df['Bathrooms'], errors='coerce')

    # Drop rows with NaN in the 'Price' column (if any)
    df = df.dropna(subset=['Price'])

    net_income = calculate_net_income(gross_income)
    suggestions = suggest_places(df, net_income)
    return render_template('result.html', net_income=net_income, suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
