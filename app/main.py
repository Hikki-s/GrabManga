import os
import tkinter as tk
from tkinter import messagebox
from path import Path
from app.config.config import config, config_file, create_conf
from app.router.router import main_router


def on_button_click():
    url = entry.get()
    try:
        answer = main_router(url)
        messagebox.showinfo('Alert', f'{answer}')
    except AttributeError:
        messagebox.showerror('Warning', 'Check the correct spelling of the link!')


def checkbox1_changed():
    if var1.get() == 1:
        config['Settings']['save_images'] = 'True'
    else:
        config['Settings']['save_images'] = 'False'

    with open(config_file, 'w') as f:
        config.write(f)


def checkbox2_changed():
    if var1.get() == 1:
        config['Settings']['pdf_merge'] = 'True'
    else:
        config['Settings']['pdf_merge'] = 'False'

    with open(config_file, 'w') as f:
        config.write(f)


def checkbox3_changed():

    if var3.get() == 1:
        config['Settings']['save_path'] = '../../'
        entry2.delete(0, tk.END)
        label2.grid_forget()
        entry2.grid_forget()
        label3.grid_forget()
    else:
        label2.grid(row=2, column=1, sticky="W")
        entry2.grid(row=2, column=2, sticky="EW")
        label3.grid(row=3, column=2, sticky="W")

    with open(config_file, 'w') as f:
        config.write(f)


def on_exit(event):
    text = entry2.get()
    if os.path.isdir(text):
        if text[-1] != '\\':
            text += '\\'

        config['Settings']['save_path'] = Path(text)
        with open(config_file, 'w') as f:
            config.write(f)

        messagebox.showinfo('Alert', f'The directory to save has been changed to:\n{text}')

    else:
        messagebox.showerror('Warning', 'Folder not found')
        entry2.delete(0, tk.END)


if __name__ == '__main__':

    create_conf()
    config.read(config_file)
    path_is_default = config.get('Settings', 'save_path') == '../../'
    window = tk.Tk()
    window.geometry('650x150')
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1, minsize=350)

    label1 = tk.Label(window, text='Link to the manga:')
    label2 = tk.Label(window, text='The path to save:')
    label3 = tk.Label(window, text='To confirm the path, press Enter!\nIf the field is empty, the directory will be set by omission\n(The directory where the application is located)')

    var1 = tk.IntVar(value=config.getboolean('Settings', 'save_images'))
    checkbox1 = tk.Checkbutton(window, text='Save images of volumes', variable=var1, command=checkbox1_changed)

    var2 = tk.IntVar(value=config.getboolean('Settings', 'pdf_merge'))
    checkbox2 = tk.Checkbutton(window, text='Combine volumes into 1 book', variable=var2, command=checkbox2_changed)

    var3 = tk.IntVar(value=path_is_default)
    checkbox3 = tk.Checkbutton(window, text='Default path', variable=var3, command=checkbox3_changed)

    button = tk.Button(window, text='Download', command=on_button_click)

    entry = tk.Entry(window)
    entry2 = tk.Entry(window)
    entry2.bind('<Return>', on_exit)

    label1.grid(row=0, column=1, sticky="W")
    entry.grid(row=0, column=2, sticky="EW")
    checkbox1.grid(row=0, column=0, sticky="W")
    checkbox2.grid(row=1, column=0, sticky="W")
    button.grid(row=3, column=0, sticky="EW")
    checkbox3.grid(row=2, column=0, sticky="W")

    if not path_is_default:
        label2.grid(row=2, column=1, sticky="W")
        entry2.insert(0, config.get('Settings', 'save_path'))
        entry2.grid(row=2, column=2, sticky="EW")
        label3.grid(row=3, column=2, sticky="W")

    window.mainloop()
