import pypokedex
import PIL.Image
import PIL.ImageTk
import tkinter as tk
import urllib3
from io import BytesIO

global current_team
current_team = ["charmander", "weedle", "charizard", "weedle", "weedle", "weedle"]


def main():
    global window
    window = tk.Tk()
    window.geometry("600x600")
    window.title("Oliver's Pokedex")
    window.config(padx=10, pady=10)

    title_label = tk.Label(window, text="Oliver's Pokedex")
    title_label.config(font=("Arial", 32))
    title_label.pack(padx=10, pady=10)

    global pokemon_image
    pokemon_image = tk.Label(window)
    pokemon_image.pack(padx=10, pady=10)

    global pokemon_information
    pokemon_information = tk.Label(window)
    pokemon_information.config(font=("Arial", 20))
    pokemon_information.pack(padx=10, pady=10)

    global pokemon_types
    pokemon_types = tk.Label(window)
    pokemon_types.config(font=("Arial", 20))
    pokemon_types.pack(padx=10, pady=10)

    global label_id_name
    label_id_name = tk.Label(window, text="ID or Name")
    label_id_name.config(font=("Arial", 20))
    label_id_name.pack(padx=10, pady=10)

    global text_id_name
    text_id_name = tk.Text(window, height=1)
    text_id_name.config(font=("Arial", 20))
    text_id_name.pack(padx=10, pady=10)

    btn_load = tk.Button(window, text="Load Pokemon", command=load_pokemon)
    btn_load.config(font=("Arial", 20))
    btn_load.pack(padx=10, pady=10)

    btn_load_team_window = tk.Button(window, text="Show Current Team", command=current_team_window)
    btn_load_team_window.config(font=("Arial", 20))
    btn_load_team_window.pack(padx=10, pady=10)
    
    window.mainloop()

def load_pokemon():
    pokemon = pypokedex.get(name=text_id_name.get(1.0, "end-1c"))

    http = urllib3.PoolManager()
    response = http.request("Get", pokemon.sprites.front.get("default"))
    image = PIL.Image.open(BytesIO(response.data))

    img = PIL.ImageTk.PhotoImage(image)
    pokemon_image.config(image=img)
    pokemon_image.image = img

    pokemon_information.config(text=f"{pokemon.dex} - {pokemon.name}")
    pokemon_types.config(text=f"{pokemon.types}")


def current_team_window():
    window.destroy()
    
    global ctw
    ctw = tk.Tk()
    ctw.geometry("600x600")
    ctw.title("Current Team")
    ctw.config(padx=10, pady=10)
    
    title_label = tk.Label(ctw, text="Current Team")
    title_label.config(font=("Arial", 32))
    title_label.pack(padx=10, pady=10)
    
    if current_team:
        # Create frames for top and bottom rows
        top_row_frame = tk.Frame(ctw)
        top_row_frame.pack(pady=10)

        bottom_row_frame = tk.Frame(ctw)
        bottom_row_frame.pack(pady=10)

        for index, pokemon_name in enumerate(current_team):
            pokemon = pypokedex.get(name=pokemon_name)

            http = urllib3.PoolManager()
            response = http.request("GET", pokemon.sprites.front.get("default"))
            image = PIL.Image.open(BytesIO(response.data))

            img = PIL.ImageTk.PhotoImage(image)
            pokemon_image = tk.Label(top_row_frame if index < 3 else bottom_row_frame, image=img)
            pokemon_image.image = img
            pokemon_image.pack(padx=10, pady=10, side="left")  # Pack the images horizontally
    
    btn_change_pokemon_1 = tk.Button(ctw, text="EDIT", width=5, command=pokemon_1)
    btn_change_pokemon_1.config(font=("Arial", 15))
    btn_change_pokemon_1.place(x=135, y=200)
    
    btn_change_pokemon_2 = tk.Button(ctw, text="EDIT", width=5, command=main)
    btn_change_pokemon_2.config(font=("Arial", 15))
    btn_change_pokemon_2.place(x=255, y=200)
    
    btn_change_pokemon_3 = tk.Button(ctw, text="EDIT", width=5, command=main)
    btn_change_pokemon_3.config(font=("Arial", 15))
    btn_change_pokemon_3.place(x=375, y=200)
    
    btn_change_pokemon_4 = tk.Button(ctw, text="EDIT", width=5, command=main)
    btn_change_pokemon_4.config(font=("Arial", 15))
    btn_change_pokemon_4.place(x=135, y=325)
    
    btn_change_pokemon_5 = tk.Button(ctw, text="EDIT", width=5, command=main)
    btn_change_pokemon_5.config(font=("Arial", 15))
    btn_change_pokemon_5.place(x=255, y=325)
    
    btn_change_pokemon_6 = tk.Button(ctw, text="EDIT", width=5, command=main)
    btn_change_pokemon_6.config(font=("Arial", 15))
    btn_change_pokemon_6.place(x=375, y=325)
    
    
    btn_back = tk.Button(ctw, text="Back To Search", command=close_current_team_window)
    btn_back.config(font=("Arial", 20))
    btn_back.place(x=180, y=400)


def pokemon_1():
    global change_pokemon_win
    change_pokemon_win = tk.Tk()
    change_pokemon_win.geometry("600x600")
    change_pokemon_win.title("Change Pokemon")
    change_pokemon_win.config(padx=10, pady=10)

    title_label_1 = tk.Label(change_pokemon_win, text="Change Pokemon")
    title_label_1.config(font=("Arial", 32))
    title_label_1.pack(padx=10, pady=10)

    pokemon_image_1 = tk.Label(change_pokemon_win)
    pokemon_image_1.pack(padx=10, pady=10)
    
    label_id_name_1 = tk.Label(change_pokemon_win, text="Name")
    label_id_name_1.config(font=("Arial", 20))
    label_id_name_1.pack(padx=10, pady=10)

    global text_id_name_1
    text_id_name_1 = tk.Text(change_pokemon_win, height=1)
    text_id_name_1.config(font=("Arial", 20))
    text_id_name_1.pack(padx=10, pady=10)

    btn_load = tk.Button(change_pokemon_win, text="Change Pokemon", command=change_pokemon_1)
    btn_load.config(font=("Arial", 20))
    btn_load.pack(padx=10, pady=10)

    btn_load_team_window = tk.Button(change_pokemon_win, text="BACK", command=current_team_window)
    btn_load_team_window.config(font=("Arial", 20))
    btn_load_team_window.pack(padx=10, pady=10)
    
def change_pokemon_1():
    pokemon = pokemon.get(name=text_id_name_1)
    current_team[0] = pokemon
    print(current_team)
        

def close_current_team_window():
    ctw.destroy()
    main()
    
def reopen_current_team_window():
    change_pokemon_win.destroy()
    current_team_window()

main()





'''
note to self
you need to finish the edit button functionality
this should allow the list to be changed based on what the user has entered
'''