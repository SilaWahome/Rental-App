# Rental-App
# Rental Application

## Overview
The Rental Application is a web app that helps users find rental apartments based on their gross income. The app calculates the Pay As You Earn (PAYE) tax, net income, and suggests rental properties within the user's budget. It also displays details like the number of bedrooms and other property information.

## Features
- **Gross Income Input**: Users can input their gross income.
- **PAYE Calculation**: Automatically calculates the PAYE tax based on Kenyan tax bands.
- **Net Income Calculation**: Computes the net income after deducting PAYE and SHIF (social health insurance fund).
- **Rental Suggestions**: Filters and displays rental properties that match the user's budget.
- **Visual Enhancements**: Displays relevant icons for each property detail (agency, neighborhood, price, and bedrooms).

## File Structure
- **app.py**: The main Flask application file that handles routing and calculations.
- **rent_apts.csv**: The CSV file containing rental property listings.
- **templates/index.html**: The HTML template for the home page.
- **templates/result.html**: The HTML template for displaying results.
- **static/styles.css**: The CSS file for styling the web pages.
- **static/images/**: Directory containing the icons for property details.

## How to Run
1. **Install Flask**:
   ```bash
   pip install flask
