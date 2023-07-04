import tkinter as tk
from tkinter import ttk, messagebox
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import requests

currencies = [
    "USD - $", "EUR - €", "JPY - ¥/円", "GBP - £", "CNY - ¥/元", "AUD - A$", "CAD - C$", "CHF", "HKD - HK$",
    "SGD - S$", "SEK - kr", "KRW - ₩/원", "NOK - kr", "NZD - NZ$", "INR - ₹", "MXN - $", "TWD - NT$", "ZAR - R",
    "BRL - R$", "DKK - kr", "PLN - zł", "THB - ฿", "ILS - ₪", "IDR -Rp", "CZK - Kč", "AED - د.إ", "TRY - ₺",
    "HUF - Ft", "CLP - CLP$", "SAR - ﷼", "PHP - ₱", "MYR - RM", "COP - COL$", "RUB - ₽", "RON - L"
]


class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="medium orchid")

        # First Combobox
        self.chosen_currency_combobox_frame = tk.Frame(self.root, bg="white")
        self.chosen_currency_combobox_frame.place(x=300, y=300)
        self.chosen_currency_combobox = ttk.Combobox(self.chosen_currency_combobox_frame, values=currencies, width=18)
        self.chosen_currency_combobox['font'] = ('Calibri', 14)
        self.chosen_currency_combobox.pack(pady=0)

        # Second Combobox
        self.target_currency_combobox_frame = tk.Frame(self.root, bg="white")
        self.target_currency_combobox_frame.place(x=300, y=400)
        self.target_currency_combobox = ttk.Combobox(self.target_currency_combobox_frame, values=currencies, width=18)
        self.target_currency_combobox['font'] = ('Calibri', 14)
        self.target_currency_combobox.pack(pady=0)

        # Input Box
        self.entry = tk.Entry(self.root, font=("Calibri", 14), width=12)
        self.entry.place(x=150, y=300)

        # 'From' Text Label
        self.input_info_label = tk.Label(self.root, text="From", font=("Calibri", 15, "bold"), bg="medium orchid", fg="white")
        self.input_info_label.place(x=150, y=260)

        # 'Convert To:' Text Label
        self.output_info_label = tk.Label(self.root, text="Convert To:", font=("Calibri", 15, "bold"), bg="medium orchid", fg="white")
        self.output_info_label.place(x=150, y=360)

        # Output (Result) Box
        self.result_box = tk.Entry(self.root, font=("Calibri", 14), width=12)
        self.result_box.place(x=150, y=400)
        self.result_box.configure(state="readonly") # User not allowed to change the result

        # Convert Button
        self.convert_button = tk.Button(self.root, text="CONVERT", command=self.convert_currency, font=("Calibri", 13, "bold"))
        self.convert_button.place(x=150, y=480)

        # Help Button
        self.help_button = tk.Button(self.root, text="HELP", command=self.show_help, font=("Calibri", 13, "bold"), width=8)
        self.help_button.place(x=240, y=480)

        # Exit Button
        self.exit_button = tk.Button(self.root, text="EXIT", command=self.exit_program, font=("Calibri", 13, "bold"), width=8)
        self.exit_button.place(x=330, y=480)

        # Swap Button
        self.swap_button = tk.Button(self.root, text="SWAP", command=self.swap_currencies, font=("Calibri", 13, "bold"), width=8)
        self.swap_button.place(x=420, y=480)

        # Canvas for the Right Side
        self.canvas = tk.Canvas(self.root, width=200, height=250, bg="#7F4AA4", highlightthickness=0)
        self.canvas.place(x=600, y=280)

        # Text in the Canvas
        self.label = tk.Label(self.canvas, text="Welcome \nto the \nCurrency \nConverter \nApp!", font=("Calibri", 18, "bold"), bg="#7F4AA4", fg="white", justify="center")
        self.label.place(x=48, y=50)

        # "Currency Converter" Image
        self.image_canvas = tk.Canvas(self.root, width=700, height=200, bg="purple", highlightthickness=0)
        self.image_canvas.place(x=100, y=30)
        self.image = Image.open("image.png")
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Filtering Combobox Results
        self.chosen_currency_combobox.bind("<KeyRelease>", self.filter_options)
        self.target_currency_combobox.bind("<KeyRelease>", self.filter_options_target)

    def convert_currency(self):
        chosen_currency = self.chosen_currency_combobox.get()[:3]
        target_currency = self.target_currency_combobox.get()[:3]
        amount = self.entry.get()

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid amount. Input must not contain commas or letters. Only numbers and a dot are accepted")
            return

        url = f"https://www.google.com/search?q={amount}+{chosen_currency}+{target_currency}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        result_div = soup.find("div", class_="BNeawe iBp4i AP7Wnd")

        if result_div is not None:
            result = result_div.text
            converted_amount = result.split()[0]  # Extract the converted amount (e.g., Instead of '328.25 Euro' -> Extract '328.25' part)
            decimal_part = float("0." + converted_amount.split(',')[1])
            converted_amount = converted_amount.split(',')[0]
        else:
            messagebox.showerror("Conversion Error", "No result found for the conversion.")
            return

        try:
            converted_amount = converted_amount.replace('.', '')
            converted_amount = float(converted_amount)

            formatted_amount = "{:,.2f}".format(converted_amount + decimal_part)

            currency_rate = converted_amount / amount
            # Displaying Currency Rate
            label_config_text = f"1 {chosen_currency} \n= \n{round(currency_rate, 3)} {target_currency}"
            self.label.configure(font=("Calibri", 15, "bold"), text=label_config_text, justify="center")
            self.label.place(x=50, y=70)

        except ValueError:
            messagebox.showerror("Conversion Error", "Invalid conversion result.")
            return

        self.result_box.configure(state='normal')
        self.result_box.delete(0, tk.END)
        self.result_box.insert(tk.END, formatted_amount)
        self.result_box.configure(state='readonly')  # User still not allowed to change the result after the convertion

    def filter_options(self, event):
        filter_value = self.chosen_currency_combobox.get().lower()
        filtered_currencies = [currency for currency in currencies if filter_value in currency.lower()]
        self.chosen_currency_combobox.configure(values=filtered_currencies)

    def filter_options_target(self, event):
        filter_value = self.target_currency_combobox.get().lower()
        filtered_currencies = [currency for currency in currencies if filter_value in currency.lower()]
        self.target_currency_combobox.configure(values=filtered_currencies)

    def show_help(self):
        messagebox.showinfo("Help", "Welcome to the Currency Converter App!\n\n"
                                    "1. Enter the amount in the 'From' field. You can use a dot for only fraction part.\n"
                                    "2. Select the currency to convert from in the 'From' dropdown.\n"
                                    "3. Select the currency to convert to in the 'Convert To' dropdown.\n"
                                    "4. Click the 'CONVERT' button to perform the conversion.\n"
                                    "5. The converted amount will be displayed in the 'Convert To' field.\n\n"
                                    "Note: Due to significant fluctuations in exchange rates between some currencies, "
                                    "the displayed currency rate on the right side may appear incorrect. To address "
                                    "this issue, you can input the value of 1 for the specific currency to retrieve its"
                                    " corresponding exchange rate accurately.")

    def exit_program(self):
        if messagebox.askokcancel("Exit", "Do you want to exit the Currency Converter App?"):
            self.root.destroy()

    def swap_currencies(self):
        chosen_currency = self.chosen_currency_combobox.get()
        target_currency = self.target_currency_combobox.get()

        self.chosen_currency_combobox.set(target_currency)
        self.target_currency_combobox.set(chosen_currency)
