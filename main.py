import sqlite3
import random
import tkinter as tk
from tkinter import messagebox

import pyperclip

# connexion à la base de donnée sqlite
db_connection = sqlite3.connect("database.sqlite")
db_cursor = db_connection.cursor()

# création d'une instance de Tk() pour créer la fenêtre
app = tk.Tk()
app.title("Générateur de mot de passe")
app.geometry("500x300")
app.resizable(width=False, height=False)

# configuration des variables de contrôle
option_latin_uppercase_letters = tk.BooleanVar(name="LatinUpperAlphabet")
option_latin_lowercase_letters = tk.BooleanVar(name="LatinLowerAlphabet")
option_arabic_numerals = tk.BooleanVar(name="ArabicNumerals")
option_punctuation_characters = tk.BooleanVar(name="PunctuationCharacters")

password = tk.StringVar()

# partie logique 
def checking_choice_options():
    """
    Fonction qui empêche de générer un mot de passe si au moins une option n'est pas cochée.
    """
    if option_latin_uppercase_letters.get() or option_latin_lowercase_letters.get() or option_arabic_numerals.get() or option_punctuation_characters.get() == True:
        btn_generate_password.config(state="normal")
        btn_copy_password.config(state="normal")
    else:
        btn_generate_password.config(state="disabled")
        btn_copy_password.config(state="disabled")


def get_password(options=(option_latin_uppercase_letters, option_latin_lowercase_letters, option_arabic_numerals, option_punctuation_characters)):
    """
    Fonction qui permet de générer le mot de passe.
    Le paramètre dispose d'une valeur par défaut : un tuple comprenant les variables de contrôle de 'tkinter'.
    Chaque variable va être associée à une colonne de la table correspondante depuis la base de données sqlite.
    Il faut cependant que le checkbutton concerné soit sélectionné pour récupérer les différentes valeurs de chaque table.
    La longueur du mot de passe est choisie par l'utilisateur en déplaçant le slider.
    Le module 'random' est ensuite utilisé pour mélanger tous les caractères.
    """
    password_elements = []

    try:
        for option in options:
            if option.get() == True:
                password_elements.extend([e[1] for e in db_cursor.execute(f"SELECT * FROM {option};")])
        password.set("".join(random.choices(password_elements, k=lenght_choice.get())))
    except:
        return None


def copy_password():
    """
    Fonction qui permet de copier le mot de passe généré au moyen de la librairie 'pyperclip'.
    """
    if password_generated.get() == "":
        messagebox.showwarning(message="Veuillez générer un mot de passe !")
    else:
        pyperclip.copy(password_generated.get())
        messagebox.showinfo(message="Le mot de passe a été copié dans le presse papier.")

# paramétrage de la fenêtre tkinter
options = tk.Frame(master=app)
options.pack(fill="x", pady=10)

latin_uppercase_letters = tk.Checkbutton(master=options, text="Lettres latines majuscules", variable=option_latin_uppercase_letters, command=checking_choice_options)
latin_uppercase_letters.grid(column=0, row=0, padx=10, pady=5)

latin_lowercase_letters = tk.Checkbutton(master=options, text="Lettres latines minuscules", variable=option_latin_lowercase_letters, command=checking_choice_options)
latin_lowercase_letters.grid(column=0, row=1, padx=10, pady=5)

arabic_numerals = tk.Checkbutton(master=options, text="Chiffres arabes", variable=option_arabic_numerals, command=checking_choice_options)
arabic_numerals.grid(column=1, row=0, padx=10, pady=5, sticky="w")

punctuation_characters = tk.Checkbutton(master=options, text="Caractères spéciaux", variable=option_punctuation_characters, command=checking_choice_options)
punctuation_characters.grid(column=1, row=1, padx=10, pady=5, sticky="w")

options_lenght = tk.Frame(master=app)
options_lenght.pack(fill="x", pady=10)

lenght_choice_label = tk.Label(master=options_lenght, text="Longueur du mot de passe : ")
lenght_choice_label.grid(column=0, row=0)

lenght_choice = tk.Scale(master=options_lenght, orient="horizontal", from_=6, to=60, length=450)
lenght_choice.grid(column=0, row=1)

option_buttons = tk.Frame(master=app)
option_buttons.pack(fill="x", pady=25)

btn_generate_password = tk.Button(master=option_buttons, text="Générer le mot de passe", command=get_password, state="disabled")
btn_generate_password.grid(column=0, row=0)

btn_copy_password = tk.Button(master=option_buttons, text="Copier le mot de passe", command=copy_password, state="disabled")
btn_copy_password.grid(column=1, row=0)

password_generated = tk.Entry(master=app, textvariable=password)
password_generated.pack(fill="x", padx=10)

# paramétrage de la grille tkinter
options.grid_columnconfigure(index=0, weight=1)
options.grid_columnconfigure(index=1, weight=1)
options_lenght.grid_columnconfigure(index=0, weight=1)
option_buttons.grid_columnconfigure(index=0, weight=1)
option_buttons.grid_columnconfigure(index=0, weight=1)
option_buttons.grid_columnconfigure(index=1, weight=1)

# affichage de la fenêtre
app.mainloop()