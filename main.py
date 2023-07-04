import tkinter as tk
import currency_converter

window = tk.Tk()
window.title("Currency Converter")
window.geometry("900x600")
window.resizable(False, False)
window.iconbitmap('icon.ico')

app = currency_converter.CurrencyConverter(window)

window.mainloop()
