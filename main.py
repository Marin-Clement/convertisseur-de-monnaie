from tkinter import *
from tkinter import ttk
import json
import requests

root = Tk()
root.resizable(False, False)
root.title("Currency Converter")
root.geometry("600x850")
root.configure(bg='white')

font = ("Arial", 14)

favorite_currencies = []
conversion_history = []


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
    conversion = f + " to " + t + ": " + amount.get() + " = " + str(round(r,3))
    add_to_history(conversion)


def save_favorite():
    favorite_currencies.append((from_currency.get(), to_currency.get()))
    favorites_listbox.insert(END, from_currency.get()+" to "+to_currency.get())
    print("Favorite currency saved: " + from_currency.get() + " to " + to_currency.get())


def use_favorite():
    selected_favorite = favorites_listbox.get(favorites_listbox.curselection())
    selected_favorite = selected_favorite.split(" to ")
    from_currency.set(selected_favorite[0])
    to_currency.set(selected_favorite[1])


def delete_favorite():
    favorites_listbox.delete(favorites_listbox.curselection())


def add_to_history(conversion):
    conversion_history.append(conversion)
    history_listbox.insert(END, conversion)


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

favorites_frame = ttk.LabelFrame(root, text="Favorite Currencies")
favorites_frame.grid(row=5, column=0, padx=10, pady=10, columnspan=2, sticky='nsew')

favorites_listbox = Listbox(favorites_frame, font=font)
favorites_listbox.grid(row=0, column=0, padx=10, pady=10)

favorites_add_button = ttk.Button(favorites_frame, text="Add", command=save_favorite)
favorites_add_button.grid(row=0, column=1, padx=10, pady=10)

favorites_use_button = ttk.Button(favorites_frame, text="Use", command=use_favorite)
favorites_use_button.grid(row=0, column=2, padx=10, pady=10)

favorites_delete_button = ttk.Button(favorites_frame, text="Delete", command=delete_favorite)
favorites_delete_button.grid(row=0, column=3, padx=10, pady=10)

history_frame = ttk.LabelFrame(root, text="Conversion History")
history_frame.grid(row=6, column=0, padx=10, pady=10, columnspan=2, sticky='nsew')

history_listbox = Listbox(history_frame, font=font, width=50)
history_listbox.grid(row=0, column=0, padx=10, pady=10)

with open('currency.json') as json_file:
    data = json.load(json_file)
    for key, value in data['symbols'].items():
        from_currency['values'] = list(data['symbols'].keys())
        to_currency['values'] = list(data['symbols'].keys())
        from_currency.set(key)
        to_currency.set(key)
    json_file.close()

root.mainloop()


"""
Ce script utilise une API pour aller chercher le rate de toutes les monnaies. Cela me permet d'avoir une quantit?? exhaustive
De currency. Malgr?? tout cela pose un probl??me pour le job bonus, car je n'utilise pas localement de moyen pour stocker
les rates. Sans utiliser d'API il suffirait de prendre une monnaie r??f??rence comme USD par exemple et de tout convertir
selon son taux de change. On pourrait donc implementer dans un fichier json tout le rate des monnaies selon l'USD.
Ici l'ajout d'une monnaie fictive serait donc bien plus simple, mais j'ai pr??f??r?? avoir un plus grande quantit?? de choix, et
un taux de change actualiser en direct
"""