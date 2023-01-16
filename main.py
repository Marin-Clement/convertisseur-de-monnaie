from tkinter import *
import requests
import json

current_from = ""
current_to = ""

root = Tk()
root.geometry("400x400")

Label(root, text="From Currency:", font=("Roboto", 30)).place(x=10, y=20)
from_currency = Menubutton(root, text=" ", width=7)
from_currency.place(x=230, y=35)
from_currency.menu = Menu(from_currency)
from_currency["menu"] = from_currency.menu
Label(root, text="To Currency:", font=("Roboto", 30)).place(x=10, y=100)
to_currency = Menubutton(root, text=" ", width=7)
to_currency.place(x=200, y=115)
to_currency.menu = Menu(to_currency)
to_currency["menu"] = to_currency.menu
Label(root, text="Amount:", font=("Roboto", 30)).place(x=10, y=180)
amount = Entry(root,width=5, bg='grey', font=("Roboto", 30))
amount.place(x=130, y=181)
Label(root, text="Result:", font=("Roboto", 30)).place(x=120, y=350)
result = Label(root, text="", font=("Roboto", 30), fg='red2')
result.place(x=215, y=351)
convert_button = Button(root, text="CONVERT", font=("Roboto", 30), bg='grey', command=lambda: calulate_diff(amount.get(),current_from,current_to))
convert_button.place(x=100, y=300)


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


def calulate_diff(amoun, f, t):
    r = float(amoun) * get_rate(f, t, amoun)
    result.config(text=round(r, 2))


def change_button_name(button, k):
    button.config(text=k)
    if button == from_currency:
        global current_from
        current_from = k
    else:
        global current_to
        current_to = k


with open('currency.json') as json_file:
    data = json.load(json_file)
    for key, value in data['symbols'].items():
        from_currency.menu.add_command(label=key, command=lambda label=key, button=from_currency: change_button_name(button, label))
        to_currency.menu.add_command(label=key, command=lambda label=key, button=to_currency:  change_button_name(button, label))
    json_file.close()


root.mainloop()
