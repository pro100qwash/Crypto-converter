# 💱 Cryptocurrency Exchange GUI App (Binance API)

This is a user-friendly cryptocurrency exchange calculator built in **Python** using the **Tkinter GUI toolkit** and **Binance API**.  
It allows users to convert between cryptocurrencies (e.g. BTC → USDT), track exchange history, and view basic rate statistics.

---

## 🧩 Features

- 🔁 Real-time cryptocurrency conversion via Binance API
- 🧮 Currency input: base, target, and amount
- 📈 Built-in history viewer and exchange rate statistics
- 💾 Local storage of conversion history in `exchange_history.json`
- 🎨 Dark-themed GUI with Binance branding
- 🧠 Automatically prevents invalid inputs and same-currency conversion

---

## 🚀 How to Run

1. Make sure Python 3.7+ is installed.

2. Clone the repository or copy the project files:
   ```bash
   git clone https://github.com/yourusername/crypto-exchange-app.git
   cd crypto-exchange-app

3. Install dependencies:
   ```bash
   pip install requests

4. Place the Binance logo image (binance.png) in the root folder (optional).

5. Run the application:
   
   ```bash
   python main.py

🎮 Interface Overview

| Component         | Function                                     |
| ----------------- | -------------------------------------------- |
| Base Currency     | Enter the original currency (e.g. BTC)       |
| Target Currency   | Enter the currency to convert to (e.g. USDT) |
| Amount            | Specify the amount to convert                |
| Convert Button    | Executes the conversion                      |
| History Button    | Opens a new window with past conversions     |
| Statistics Button | Shows max, min, and average rates            |
| Result Label      | Displays converted value                     |

📂 Files Overview

| File                    | Description                          |
| ----------------------- | ------------------------------------ |
| `main.py`               | Full source code (GUI, logic, API)   |
| `exchange_history.json` | Stores local history of conversions  |
| `binance.png`           | Optional logo image (appears in GUI) |
| `README.md`             | Project description                  |

🧠 Code Structure

📦 Classes

`ExchangeBase`

Loads and saves exchange history

Provides statistics: min, max, average

`CryptoCurrencyExchange (inherits from ExchangeBase)`

Communicates with Binance API

Handles conversion logic

Supports indirect conversion via USDT if needed

`CurrencyExchangeApp`

Handles all Tkinter UI elements

Contains logic for displaying results, history, and stats


🖼 Screenshot

![image](https://github.com/user-attachments/assets/6187a1ef-f5ba-4630-b4d7-baab3e0f0701)

![image](https://github.com/user-attachments/assets/881e9389-de21-44e0-a82b-2a7353d0e97a)

![image](https://github.com/user-attachments/assets/31848616-32d7-43c6-a94d-9014113581f2)


⚠️ Notes

Works only with currency pairs available on Binance.

Indirect conversion is done via USDT when a direct pair is not supported.

Make sure you are connected to the internet to fetch exchange rates.

📜 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute.

👨‍💻 Author

Developed by Ivan Efimov
