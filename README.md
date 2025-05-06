💱 Currency Exchange GUI App (Binance API)
A simple Python GUI application for cryptocurrency exchange using the Binance API. This app allows you to:

Fetch real-time exchange rates for cryptocurrencies.

Convert between different currencies.

Store a history of your exchanges.

View exchange rate statistics (maximum, minimum, average).

🖼 Interface
The application uses Tkinter to provide a modern dark-themed graphical interface. It includes:

Input fields for base and target currencies.

Real-time conversion using Binance rates.

Conversion result display.

History and statistics buttons.

A Binance logo embedded into the UI.

📦 Dependencies
Python 3.7+

requests — for HTTP requests to the Binance API.

tkinter — for GUI (built-in with most Python distributions).

To install required dependencies:

pip install requests

🚀 How to Run

Make sure Python 3.7 or higher is installed.

Clone the repository:

bash
Копировать
Редактировать
git clone https://github.com/yourusername/currency-exchange-app.git
cd currency-exchange-app
Run the application:

bash
Копировать
Редактировать
python main.py
🛠 Code Structure
ExchangeBase
Handles storage and retrieval of exchange history and statistical calculations.

CryptoCurrencyExchange
Inherits ExchangeBase. Responsible for interacting with the Binance API and calculating conversion rates.

CurrencyExchangeApp
The Tkinter GUI class. Handles all user input, output, and interaction.

exchange_history.json
Stores local history of all conversions made via the app.

📊 Features
✅ Real-time cryptocurrency conversion using Binance.

✅ Conversion history saved locally to JSON.

✅ History viewer with timestamps and values.

✅ Statistics calculation: max, min, average rates.

✅ Dark-themed modern GUI.

🖼 Screenshot

![image](https://github.com/user-attachments/assets/b0198dc0-f040-4f6e-8c52-5a646771f983)


⚠️ Notes
Works only with currency pairs available on Binance.

Indirect conversion is done via USDT when a direct pair is not supported.

Make sure you are connected to the internet to fetch exchange rates.

👨‍💻 Author
Developed by Ivan Efimov
