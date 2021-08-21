from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def search_through_website():
    website = website_input.get()
    if len(website) == 0:
        messagebox.showinfo(title='Oopsy', message='Please enter the name of the website you want to search your'
                            ' credentials for.')
    else:
        try:
            with open('data.json', mode='r') as f:
                data = json.load(f)
            email = data[website]["email"]
            password = data[website]["password"]
        except FileNotFoundError:
            messagebox.showinfo(title='Missing file', message='There is no previous data to fetch information from.')
        except KeyError:
            messagebox.showinfo(title='Info not found', message='There is no information on your credentials for the '
                                'website you are searching for.')
        else:
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")


def generate_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    l = [random.choice(letters) for i in range(nr_letters)]
    s = [random.choice(symbols) for j in range(nr_symbols)]
    n = [random.choice(numbers) for k in range(nr_numbers)]

    password_list = l+s+n

    random.shuffle(password_list)

    password = ''.join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            'email': email,
            'password': password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please do not leave any of the fields empty.")
    else:
        try:
            with open('data.json', mode='r') as f:
                data = json.load(f)
                data.update(new_data)
        except FileNotFoundError:
            with open('data.json', mode='w') as f:
                json.dump(new_data, f, indent=4)
        else:
            with open('data.json', mode='w') as f:
                json.dump(data, f, indent=4)

        website_input.delete(0, END)
        email_input.delete(0, END)
        password_input.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
password_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=password_img)
canvas.grid(column=1, row=0)

website_label = Label(text='Website:')
website_label.grid(column=0, row=1)

email_label = Label(text='Email/Username:')
email_label.grid(column=0, row=2)

password_label = Label(text='Password:')
password_label.grid(column=0, row=3)

website_input = Entry(width=21)
website_input.grid(column=1, row=1)
website_input.focus()

email_input = Entry(width=35)
email_input.grid(column=1, row=2, columnspan=2)

password_input = Entry(width=21)
password_input.grid(column=1, row=3)

generator_label = Button(text='Generate Password', command=generate_password)
generator_label.grid(column=2, row=3)

search_button = Button(text='Search', command=search_through_website, width=14)
search_button.grid(column=2, row=1)

add_button = Button(text='Add', width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
