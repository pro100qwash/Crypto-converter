import json
import os
import requests
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, PhotoImage


class ExchangeBase:
    """
    Základní třída pro práci s výměnou měn a historií operací.

    Metody:
    - save_to_history: Uložení operace do historie.
    - save_history: Uložení historie do souboru.
    - load_history: Načtení historie z externího souboru.
    - get_statistics: Získání statistik směnných kurzů.
    """
    def __init__(self):
        self.history_file = "exchange_history.json"  # Název souboru pro ukládání historie
        self.exchange_history = self.load_history()  # Načítání historie při startu aplikace

    def save_to_history(self, base_currency, target_currency, rate, amount, converted_amount):
        """
        Uložení operace do historie směn.

        Parametry:
        - base_currency (str): Výchozí měna pro konverzi.
        - target_currency (str): Cílová měna pro konverzi.
        - rate (float): Aktuální směnný kurz.
        - amount (float): Částka k převedení.
        - converted_amount (float): Převedená částka.
        """
        # Přidání nové operace do seznamu historie
        self.exchange_history.append({
            "timestamp": datetime.now().isoformat(),  # Čas, kdy byla operace provedena
            "base_currency": base_currency,
            "target_currency": target_currency,
            "rate": rate,
            "amount": amount,
            "converted_amount": converted_amount
        })
        self.save_history()   # Uložení aktualizované historie

    def save_history(self):
        """Uložení historie výměn do souboru."""
        with open(self.history_file, "w", encoding="utf-8") as file:  # Zápis dat do JSON souboru s formátováním
            json.dump(self.exchange_history, file, indent=4)

    def load_history(self):
        """Načtení historie ze souboru."""
        if os.path.exists(self.history_file):  # Kontrola existence souboru
            try:
                with open(self.history_file, "r", encoding="utf-8") as file:   # Načtení dat ze souboru
                    return json.load(file)
            except Exception:
                messagebox.showwarning("Error", "Failed to load history. File is corrupted.")
        return []

    def get_statistics(self, base_currency, target_currency):
        """
        Výpočet statistik směnných kurzů.

        Parametry:
        - base_currency (str): Výchozí měna.
        - target_currency (str): Cílová měna.

        Návratová hodnota:
        - (dict): Slovník obsahující max, min a průměr směnného kurzu.
        """
        rates = [entry["rate"]
            for entry in self.exchange_history   # Filtrace operací odpovídajících měnám
            if entry["base_currency"] == base_currency and entry["target_currency"] == target_currency]
        if not rates:
            raise Exception(f"No data available for {base_currency} -> {target_currency}.")
        return {
            "max_rate": max(rates),
            "min_rate": min(rates),
            "avg_rate": sum(rates) / len(rates)}

# ================================
# Třída CryptoCurrencyExchange
# ================================

class CryptoCurrencyExchange(ExchangeBase):
    """
    Třída pro práci s výměnou kryptoměn.

    Dědí z ExchangeBase a přidává metody pro získání směnných kurzů
    a konverzi kryptoměn.
    """
    def __init__(self):
        super().__init__()  # Inicializace základní třídy
        self.api_url = "https://api.binance.com/api/v3/ticker/price"

    def get_exchange_rate(self, base_currency, target_currency):
        """
        Získání aktuálního směnného kurzu.

        Parametry:
        - base_currency (str): Výchozí měna (např. BTC)
        - target_currency (str): Cílová měna (např. USDT)

        Návratová hodnota:
        - (float): Aktuální směnný kurz.
        """
        symbol = f"{base_currency}{target_currency}" if base_currency != "USDT" else f"{target_currency}{base_currency}"
        try:
            response = requests.get(self.api_url, params={"symbol": symbol})
            response.raise_for_status()
            price = float(response.json()["price"])
            return 1 / price if base_currency == "USDT" else price
        except Exception as e:
            raise Exception(f"Error getting rate for {base_currency} -> {target_currency}: {e}")

    def convert_currency(self, base_currency, target_currency, amount):
        """
        Provádí konverzi měny mezi zvolenými měnami.

        Parametry:
        - base_currency (str): Výchozí měna.
        - target_currency (str): Cílová měna.
        - amount (float): Částka k převodu.

        Návratová hodnota:
        - converted_amount(float): Převedená částka.
        """
        try:
            if base_currency == target_currency:
                raise ValueError("Base and target currencies cannot be the same.")

            # Přímý pár
            if base_currency == "USDT" or target_currency == "USDT":
                rate = self.get_exchange_rate(base_currency, target_currency)
            else:
                # Konverze přes USDT
                rate_to_usdt = self.get_exchange_rate(base_currency, "USDT")
                rate_from_usdt = self.get_exchange_rate("USDT", target_currency)
                rate = rate_to_usdt * rate_from_usdt

            converted_amount = amount * rate
            self.save_to_history(base_currency, target_currency, rate, amount, converted_amount)
            return converted_amount
        except Exception as e:
            raise Exception(f"Conversion error: {e}")

# ================================
# Třída CurrencyExchangeApp
# ================================
class CurrencyExchangeApp:
    """
    Třída pro vytvoření grafického rozhraní aplikace směny měn.
    """

    def __init__(self, root):
        """
        Inicializuje hlavní okno aplikace a potřebné komponenty.

        Parametry:
        - root (tk.Tk): Hlavní okno aplikace.
        """

        self.exchange = CryptoCurrencyExchange()   # Instance třídy pro výměnu kryptoměn
        self.root = root
        self.root.title("Currency Exchange Calculator")
        self.root.geometry("500x250")
        self.root.resizable(False, False)   # Zakázání změny velikosti okna
        self.root.configure(bg="#333")  # Nastavení barvy pozadí
        self.create_widgets()

    def create_widgets(self):
        """
        Vytvoří widgety aplikace.
        """
        frame = tk.Frame(self.root, bg="#333", padx=10, pady=10)  # Pozadí kontejneru
        frame.grid(row=0, column=0, sticky="nsew")   # Umístění kontejneru

        self.root.grid_columnconfigure(0, weight=1)  # Konfigurace sloupců
        self.root.grid_rowconfigure(0, weight=1)  # Konfigurace řádků

        # Vstupní pole a štítky
        tk.Label(frame, text="Base currency:", bg="#333", fg="white").grid(row=0, column=0, pady=5, sticky="w")
        self.base_currency_entry = tk.Entry(frame, width=10, bg="#444", fg="white", insertbackground="white")
        self.base_currency_entry.grid(row=0, column=1, pady=5, sticky="w")

        tk.Label(frame, text="Target currency:", bg="#333", fg="white").grid(row=1, column=0, pady=5, sticky="w")
        self.target_currency_entry = tk.Entry(frame, width=10, bg="#444", fg="white", insertbackground="white")
        self.target_currency_entry.grid(row=1, column=1, pady=5, sticky="w")

        tk.Label(frame, text="Amount:", bg="#333", fg="white").grid(row=2, column=0, pady=5, sticky="w")
        self.amount_entry = tk.Entry(frame, width=10, bg="#444", fg="white", insertbackground="white")
        self.amount_entry.grid(row=2, column=1, pady=5, sticky="w")

        # Tlačítko "Convert"
        tk.Button(frame, text="Convert", command=self.convert_currency, bg="#555", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

        # Výsledek konverze
        self.result_label = tk.Label(frame, text="", bg="#333", fg="#f0b90b")
        self.result_label.grid(row=4, column=0, columnspan=2)

        # Tlačítka pro historii a statistiku
        tk.Button(frame, text="History", command=self.show_history, bg="#555", fg="white").grid(row=5, column=0, pady=5, sticky="w")
        tk.Button(frame, text="Statistics", command=self.show_statistics, bg="#555", fg="white").grid(row=5, column=1, pady=5, sticky="w")

        # Přidání obrázku na stranu
        self.image = PhotoImage(file="binance.png").subsample(2, 2)
        image_label = tk.Label(self.root, image=self.image, bg="#333")
        image_label.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

    def convert_currency(self):
        """
        Zpracuje konverzi měn podle zadaných parametrů.

        Vstupní proměnné:
        - base (str): Kód výchozí měny.
        - target (str): Kód cílové měny.
        - amount (float): Částka k převodu.
        """
        try:
            base = self.base_currency_entry.get().strip().upper()  # Získání výchozí měny
            target = self.target_currency_entry.get().strip().upper()  # Získání cílové měny
            amount = float(self.amount_entry.get().strip())
            if not base or not target or amount <= 0:  # Kontrola, zda jsou všechny vstupy platné
                raise ValueError("Invalid input.")
            result = self.exchange.convert_currency(base, target, amount)
            self.result_label.config(text=f"{amount} {base} = {result:.2f} {target}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_history(self):
        """
        Zobrazí historii operací směn v novém okně.

        Proměnné:
        - history_window (tk.Toplevel): Nové okno, kde je zobrazena historie.
        - history (list): Historie směn záznamů.
        """
        history_window = tk.Toplevel(self.root)  # Vytvoření nového okna pro historii
        history_window.title("Exchange History")
        history_window.configure(bg="#333")  # Šedé pozadí okna historie
        history = self.exchange.exchange_history
        if not history:
            tk.Label(history_window, text="No history available.", bg="#333", fg="white").pack(pady=10)
        else:
            for entry in history:   # Pro každý záznam v historii
                tk.Label(history_window, text=f"{entry['timestamp']}: {entry['amount']} {entry['base_currency']} -> "
                                              f"{entry['converted_amount']:.2f} {entry['target_currency']}",
                         bg="#333", fg="white").pack()   # Zobrazení záznamu

    def show_statistics(self):
        """
        Zobrazí statistiky směnných kurzů v dialogovém okně.

        Proměnné:
        - base (str): Kód výchozí měny (zadává uživatel).
        - target (str): Kód cílové měny (zadává uživatel).
        - stats (dict): Statistiky směnného kurzu (maximální, minimální, průměrné hodnoty).
        """
        try:
            base = self.base_currency_entry.get().strip().upper()
            target = self.target_currency_entry.get().strip().upper()
            stats = self.exchange.get_statistics(base, target)
            messagebox.showinfo("Statistics",
                                f"Max: {stats['max_rate']:.4f}\nMin: {stats['min_rate']:.4f}\nAverage: {stats['avg_rate']:.4f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    CurrencyExchangeApp(root)
    root.mainloop()