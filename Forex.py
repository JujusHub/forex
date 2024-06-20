from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Define your API key and base URL for ExchangeRatesAPI.io
API_KEY = 'fb4f6eeb4dbcf749c9438e3ee1952f85'
BASE_URL = f'https://v6.exchangeratesapi.io/latest?access_key={API_KEY}'

# Define currencies you want to support for conversion
SUPPORTED_CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY']  # Add more as needed

# HTML templates
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Forex Converter</title>
</head>
<body>
    <h1>Forex Converter</h1>
    <form action="/convert" method="post">
        <label for="amount">Amount:</label>
        <input type="text" id="amount" name="amount"><br><br>
        
        <label for="from_currency">From Currency:</label>
        <select id="from_currency" name="from_currency">
            {}
        </select><br><br>
        
        <label for="to_currency">To Currency:</label>
        <select id="to_currency" name="to_currency">
            {}
        </select><br><br>
        
        <input type="submit" value="Convert">
    </form>
</body>
</html>
"""

result_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Conversion Result</title>
</head>
<body>
    <h1>Conversion Result</h1>
    <p>Converted {} {} to {}:</p>
    <h2>{}</h2>
    <br>
    <a href="/"><button>Convert Another</button></a>
</body>
</html>
"""

# Route for the main form
@app.route('/')
def index():
    from_currency_options = ''.join(f'<option value="{currency}">{currency}</option>' for currency in SUPPORTED_CURRENCIES)
    to_currency_options = ''.join(f'<option value="{currency}">{currency}</option>' for currency in SUPPORTED_CURRENCIES)
    
    return index_html.format(from_currency_options, to_currency_options)

# Route to handle form submission and display results
@app.route('/convert', methods=['POST'])
def convert():
    try:
        amount = float(request.form['amount'])
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']

        # Construct the API request URL
        api_url = f'{BASE_URL}&base={from_currency}&symbols={to_currency}'

        response = requests.get(api_url)
        data = response.json()

        if response.status_code != 200:
            return f"Error fetching data: {data['error']['message']}"
        
        if data['success']:
            rate = data['rates'][to_currency]
            converted_amount = amount * rate
            return result_html.format(amount, from_currency, to_currency, converted_amount)
        else:
            return f"Conversion failed: {data['error']['type']} - {data['error']['info']}"

    except (KeyError, ValueError) as e:
        return f"Error: {str(e)}"

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {str(e)}"

# Route to go back to the main form
@app.route('/back')
def back():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)