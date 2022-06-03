import cv2
import pickle
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from os import path, remove
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

AUTHENTICATED = False

IMAGE = None
IMAGE_LOADED = False
#
FILETYPE = (('PNG File','*.png'),('JPEG File','*.jpg'),('All Files','*') )
# FILETYPE = (('PNG File','*.png'))

# FILETYPE = (('PNG File','*.png') )
LABEL_FONT = ('Comic sans MS', 13, 'bold')
BUTTON_FONT = ('Arial black', 10, 'bold')

image_frame = None
img_button = None
encode = None
decode = None

x = None
y = None

pass_var = None


def get_data():
    global root, pass_var, question_var, answer_var, key_var

    root = tk.Tk()
    root.title('Hide Text in Image GUI App')
    root.geometry('800x500')
    root.resizable(0, 0)

    pass_var = tk.StringVar()
    question_var = tk.StringVar()
    answer_var = tk.StringVar()
    key_var = tk.StringVar()

    frame = tk.Frame(root, width=800, height=500, bg='powderblue')
    frame.pack()

    label = tk.Label(frame, text='Setting up for the first use...', font=('Comic sans MS', 25, 'bold'),
                     fg='blue', bg='powderblue')
    label.place(relx=0.20, rely=0.05)

    label = tk.Label(frame, text='Enter your password (Used to login on start of the application)',
                     font=LABEL_FONT, fg='green', bg='powderblue')
    label.place(relx=0.17, rely=0.25)
    password = tk.Entry(frame, textvar=pass_var, show='*', width=20, font=('Times new Roman', 13), justify='center')
    password.place(relx=0.37, rely=0.32)
    password.focus_set()

    message = 'Enter security question and answer (This has to be answered when resetting password)'
    label = tk.Label(frame, text=message, font=LABEL_FONT, fg='green', bg='powderblue')
    label.place(relx=0.04, rely=0.43)
    tk.Label(frame, text='Question : ', font=LABEL_FONT, fg='blue', bg='powderblue').place(relx=0.33, rely=0.50)
    question = tk.Entry(frame, textvar=question_var, width=20, font=('Times new Roman', 13), justify='center')
    question.place(relx=0.46, rely=0.51)
    tk.Label(frame, text=' Answer  : ', font=LABEL_FONT, fg='blue', bg='powderblue').place(relx=0.33, rely=0.56)
    answer = tk.Entry(frame, textvar=answer_var, show='*', width=20, font=('Times new Roman', 13), justify='center')
    answer.place(relx=0.46, rely=0.57)

    label = tk.Label(frame, text='Enter your encryption key (3-6 characters long)', font=LABEL_FONT,
                     fg='green', bg='powderblue')
    label.place(relx=0.24, rely=0.68)
    password = tk.Entry(frame, textvar=key_var, width=20, font=('Times new Roman', 13), justify='center')
    password.place(relx=0.37, rely=0.75)

    button = tk.Button(frame, text='Configure', command=save_data, font=BUTTON_FONT, fg='white', bg='red')
    button.place(relx=0.43, rely=0.85)

    root.mainloop()


def save_data():
    global data, x, y

    temp_data = {
        'password': pass_var.get(),
        'question': question_var.get(),
        'answer': answer_var.get(),
        'key': key_var.get()
    }

    if temp_data['password'] == '':
        messagebox.showerror(title='Password empty', message='Passwords cannot be empty. Please try again!')
        return

    if temp_data['question'] == '' or temp_data['answer'] == '':
        message = 'The question and answer fields are mandatory. Please fill them and try again'
        messagebox.showerror(title='Empty Fields', message=message)
        return

    l = len(temp_data['key'])
    if l == 0:
        messagebox.showerror(title='Key error', message='Key cannot be empty. Please try again!')
        return
    if l < 3 or l > 6:
        message = 'The key provided is either too long or too short. Please try again!'
        messagebox.showerror(title='Key error', message=message)
        return

    data['initialized_user'] = True
    data.update(temp_data)

    with open('config.pickle', 'wb') as f:
        pickle.dump(data, f)

    message = 'Successfully saved user configuration! You will be prompted to enter password from the next time!'
    messagebox.showinfo(title='Configuration successful', message=message)

    x, y = root.winfo_x(), root.winfo_y()

    root.quit()
    root.destroy()


def open_screen(event):
    global root, x, y, pass_var

    try:
        x, y = root.winfo_x(), root.winfo_y()
        root.quit()
        root.destroy()
    except:
        pass

    root = tk.Tk()
    root.title('Hide Text in Image GUI App')

    if x is not None:
        root.geometry(f'800x500+{x}+{y}')
    else:
        root.geometry('800x500')

    root.resizable(0, 0)

    pass_var = tk.StringVar()

    frame = tk.Frame(root, width=800, height=500, bg='powderblue')
    frame.pack()

    label = tk.Label(frame, text='Enter password', font=('Comic sans MS', 25, 'bold'), fg='green', bg='powderblue')
    label.place(relx=0.33, rely=0.38)
    password = tk.Entry(frame, textvar=pass_var, show='*', width=20, font=('Times new Roman', 15), justify='center')
    password.place(relx=0.36, rely=0.50)

    password.focus_set()
    password.bind('<Return>', check_password)

    label = tk.Label(frame, text='Forgot password ?', cursor='hand2', font='Arial 11 underline', bg='powderblue')
    label.place(relx=0.40, rely=0.58)
    label.bind('<Button-1>', forgot_password)
    root.mainloop()


def forgot_password(event):
    global root, x, y, answer_var

    x, y = root.winfo_x(), root.winfo_y()
    root.quit()
    root.destroy()

    root = tk.Tk()
    root.title('Hide Text in Image GUI App')
    root.geometry(f'800x500+{x}+{y}')
    root.resizable(0, 0)

    answer_var = tk.StringVar()

    frame = tk.Frame(root, width=800, height=500, bg='powderblue')
    frame.pack()

    label = tk.Label(frame, text='Question : ' + data['question'], font=LABEL_FONT, bg='powderblue', justify='center')
    label.place(relx=0.35, rely=0.4)
    tk.Label(frame, text=' Answer  : ', font=LABEL_FONT, bg='powderblue', justify='center').place(relx=0.35, rely=0.45)
    answer = tk.Entry(frame, textvar=answer_var, show='*', width=20, font=('Times new Roman', 13), justify='center')
    answer.place(relx=0.47, rely=0.46)
    answer.bind('<Return>', check_answer)

    label = tk.Label(frame, text='Back to login screen', cursor='hand2', font='Arial 11 underline', bg='powderblue')
    label.place(relx=0.40, rely=0.58)
    label.bind('<Button-1>', open_screen)
    root.mainloop()


def check_answer(event):
    global root, x, y

    answer = answer_var.get()

    if answer == '':
        messagebox.showerror(title='Empty Field', message='Answer cannot be empty. Please try again!')
        return

    if answer.lower() != data['answer'].lower():
        messagebox.showerror(title='Authentication Failed', message='That answer is incorrect. Please try again!')
        return

    x, y = root.winfo_x(), root.winfo_y()
    root.quit()
    root.destroy()

    reset_password()


def reset_password():
    global root, pass_var

    root = tk.Tk()
    root.title('Hide Text in Image GUI App')
    root.geometry(f'800x500+{x}+{y}')
    root.resizable(0, 0)

    pass_var = tk.StringVar()

    frame = tk.Frame(root, width=800, height=500, bg='powderblue')
    frame.pack()

    label = tk.Label(frame, text='Enter new password', font=('Comic sans MS', 25, 'bold'), fg='green', bg='powderblue')
    label.place(relx=0.29, rely=0.38)
    password = tk.Entry(frame, textvar=pass_var, show='*', width=20, font=('Times new Roman', 15), justify='center')

    password.place(relx=0.36, rely=0.50)
    password.bind('<Return>', save_password)
    root.mainloop()


def save_password(event):
    global data

    password = pass_var.get()

    if password == '':
        messagebox.showerror(title='Password empty', message='Passwords cannot be empty. Please try again!')
        return

    data['password'] = password
    remove('config.pickle')
    with open('config.pickle', 'wb') as f:
        pickle.dump(data, f)

    messagebox.showinfo(title='Operation Successful', message='Password changed successfully')

    open_screen(None)


def check_password(event):
    global AUTHENTICATED, x, y

    if pass_var.get() != data['password']:
        messagebox.showerror(title='Login Failed', message='That password is incorrect. Please try again.')
        return

    AUTHENTICATED = True

    x, y = root.winfo_x(), root.winfo_y()

    root.quit()
    root.destroy()


def init_gui():
    global root, x, y, image_frame, img_button, encode, decode

    root = tk.Tk()
    root.title('Hide Text in Image GUI App')
    root.geometry(f'800x500+{x}+{y}')
    root.resizable(0, 0)

    frame = tk.Frame(root, width=800, height=500, bg='powderblue')
    frame.pack()

    image_frame = tk.Frame(frame, width=400, height=400, bg='grey', borderwidth=6, relief=tk.RIDGE)
    img_button = tk.Button(image_frame, text='Click here to choose image', command=load_img)
    image_frame.place(relx=0.48, rely=0.10)
    img_button.place(relx=0.33, rely=0.45)

    nb = ttk.Notebook(frame, width=350, height=400)
    nb.place(relx=0.02, rely=0.08)

    encode_frame = tk.Frame(nb)
    tk.Label(encode_frame, text='Enter message here:', font=LABEL_FONT, fg='blue').place(relx=0.23, rely=0.05)
    input_frame = tk.Frame(encode_frame, width=325, height=210)
    encode = tk.Text(input_frame)
    button = tk.Button(encode_frame, text='Encrypt', command=encrypt, width=10, font=BUTTON_FONT, fg='white', bg='red')
    input_frame.place(relx=0.04, rely=0.15)
    encode.place(relx=0, rely=0)
    button.place(relx=0.34, rely=0.7)

    decode_frame = tk.Frame(nb)
    button = tk.Button(decode_frame, text='Decrypt', command=decrypt, width=10, font=BUTTON_FONT, fg='white', bg='red')
    text_frame = tk.Frame(decode_frame, width=325, height=210)
    decode = tk.Text(text_frame, state=tk.DISABLED)
    button.place(relx=0.34, rely=0.05)
    text_frame.place(relx=0.04, rely=0.17)
    decode.place(relx=0, rely=0)

    nb.add(encode_frame, text='Encode')
    nb.add(decode_frame, text='Decode')

    root.mainloop()


def load_img():
    global IMAGE, IMAGE_LOADED

    img = filedialog.askopenfile(initialdir='/', title='Choose image file', filetypes=FILETYPE)

    if img is not None:
        IMAGE = img.name
        IMAGE_LOADED = True

        img = Image.open(IMAGE)
        img = img.resize((350, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        picture = tk.Label(image_frame, image=img)
        picture.image = img
        picture.place(relx=0.045, rely=0.05)
        img_button.config(text='Change Image')
        img_button.place(relx=0.4, rely=0.75)


def binary(data):
    if isinstance(data, str):
        return ''.join([format(ord(i), '08b') for i in data])

    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, '08b') for i in data]

    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, '08b')

    return None


def encrypt():
    if IMAGE_LOADED is False:
        messagebox.showerror(title='Image not selected', message='Please choose an image to encrypt!')
        return

    img = cv2.imread(IMAGE)
    message = encode.get('1.0', tk.END)
    max_bytes = img.shape[0] * img.shape[1] * 3 // 8

    if len(message) > max_bytes:
        message = 'More bytes required to encode this data. Try with a larger image'
        messagebox.showerror(title='Insufficient bytes!', message=message)
        return

    message += data['key']
    data_index = 0

    plain_text = binary(message)
    length = len(plain_text)

    for i in img:
        for pixel in i:
            r, g, b = binary(pixel)

            if data_index < length:
                pixel[0] = int(r[:-1] + plain_text[data_index], 2)
                data_index += 1

            if data_index < length:
                pixel[1] = int(g[:-1] + plain_text[data_index], 2)
                data_index += 1

            if data_index < length:
                pixel[2] = int(b[:-1] + plain_text[data_index], 2)
                data_index += 1

            if data_index >= length:
                break

    file = filedialog.asksaveasfilename(initialdir='/', title='Choose save location', filetypes=FILETYPE)
    file += '.png'
    # file += '.jpeg'
    print(FILETYPE, "This is a file type")
    # file += '.png'
    cv2.imwrite(file, img)
    messagebox.showinfo(title='Operation Successful', message='Data encrypted successfully')


def decrypt():
    global decode

    if IMAGE_LOADED is False:
        messagebox.showerror(title='Image not selected', message='Please choose an image to encrypt!')
        return

    bin_str = ''
    img = cv2.imread(IMAGE)

    for i in img:
        for pixel in i:
            r, g, b = binary(pixel)
            bin_str += r[-1] + g[-1] + b[-1]

    img_bytes = [bin_str[i: i + 8] for i in range(0, len(bin_str), 8)]

    message = ''
    key = data['key']
    l = len(key)
    for b in img_bytes:
        message += chr(int(b, 2))
        if message[-l:] == key:
            break

    message = message[: -l]

    decode.config(state=tk.NORMAL)
    decode.delete('1.0', tk.END)
    decode.insert(tk.END, message)
    decode.config(state=tk.DISABLED)

    messagebox.showinfo(title='Operation Successful', message='Data decrypted successfully')


if __name__ == '__main__':
    if not path.exists('config.pickle'):
        data = {'initialized_user': False, 'password': '', 'question': '', 'answer': '', 'key': ''}

    else:
        with open('config.pickle', 'rb') as f:
            data = pickle.load(f)

    if not data['initialized_user']:
        get_data()

        if data['initialized_user']:
            init_gui()

    else:
        open_screen(None)

        if AUTHENTICATED:
            init_gui()