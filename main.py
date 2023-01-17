from tkinter import *
from tkinter import ttk
import json
import requests


root = Tk()
root.title("Converter")
root.geometry("550x300")
root.configure(bg='white')


font = ("Arial", 14)

favorite_currencies = []


def get_rate(f, t, a):
    url = "https://api.apilayer.com/fixer/convert?to=" + str(t) + "&from=" + str(f) + "&amount=" + str(a)

    payload = {}
    headers = {
      "apikey": "dODkjRPLrzJ079J5TtXIWypbygLxauwG"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    result_json = json.loads(response.text)
    rate = result_json['info']['rate']

    return float(rate)


def calculate_diff(amoun, f, t):
    r = float(amoun) * get_rate(f, t, amoun)
    result.config(text=round(r, 3))


def save_favorite():
    favorite_currencies.append((from_currency.get(), to_currency.get()))
    print("Favorite currency saved: " + from_currency.get() + " to " + to_currency.get())


def use_favorite():
    if not favorite_currencies:
        print("No favorite currencies saved.")
        return
    from_currency.set(favorite_currencies[-1][0])
    to_currency.set(favorite_currencies[-1][1])


from_label = ttk.Label(root, text="From Currency:", font=font, background='white')
from_label.grid(row=0, column=0, padx=10, pady=10)


from_currency = ttk.Combobox(root, font=font)
from_currency.grid(row=0, column=1, padx=10, pady=10)


to_label = ttk.Label(root, text="To Currency:", font=font, background='white')
to_label.grid(row=1, column=0, padx=10, pady=10)


to_currency = ttk.Combobox(root, font=font)
to_currency.grid(row=1, column=1, padx=10, pady=10)


amount_label = ttk.Label(root, text="Amount:", font=font, background='white')
amount_label.grid(row=2,column=0, padx=10, pady=10)


amount = ttk.Entry(root, font=font)
amount.grid(row=2, column=1, padx=10, pady=10)


convert_button = ttk.Button(root, text="CONVERT", command=lambda: calculate_diff(amount.get(), from_currency.get(), to_currency.get()))
convert_button.grid(row=3, column=0, padx=10, pady=10)


result_label = ttk.Label(root, text="Result:", font=font, background='white')
result_label.grid(row=4, column=0, padx=10, pady=10)


result = ttk.Label(root, text="", font=font, background='white', foreground='red')
result.grid(row=4, column=1, padx=10, pady=10)


save_favorite_button = ttk.Button(root, text="SAVE AS FAVORITE", command=save_favorite)
save_favorite_button.grid(row=0, column=2, padx=10, pady=10)


use_favorite_button = ttk.Button(root, text="USE FAVORITE", command=use_favorite)
use_favorite_button.grid(row=1, column=2, padx=10, pady=10)


with open('currency.json') as json_file:
    data = json.load(json_file)
    for key, value in data['symbols'].items():
        from_currency['values'] = list(data['symbols'].keys())
        to_currency['values'] = list(data['symbols'].keys())
        from_currency.set(key)
        to_currency.set(key)
    json_file.close()



root.mainloop()
