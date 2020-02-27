from tkinter import *
from tkinter import filedialog
import pandas as pd

window = Tk()
window.title('K Modes Alpha H')
window.geometry('2500x1500')

label1 = Label(window, text='Select a CSV file for upload:', anchor=CENTER)
label2 = Label(window, text='Enter label number for first aligned attribute\n (the actual sequence location '
                            'of the first aligned column):', anchor=CENTER)
label3 = Label(window, text='Set what percentage of insertion data to exclude\n', anchor=CENTER)

label4 = Label(window, text='\nSet Sr(mode) cutoff value.\nRecommended start value is 0.15.\n\n '
                            'Changing the value will increase or \n '
                            'decrease resolution of the tree:', anchor=CENTER)

t = Text(window, height=25, width=85, bg='black', fg='#76EE00')
t.grid(column=2, row=11)

label1.grid(column=0, row=0)
label2.grid(column=0, row=3)
label3.grid(column=0, row=5)
label4.grid(column=2, row=2)


label_number = IntVar()
label_number.set(1)
cut_off = DoubleVar()
cut_off.set(.15)
null_filter = DoubleVar()
null_filter.set(.12)

entry1 = Entry(width=30)
entry2 = Entry(width=3, textvariable=label_number)
entry3 = Entry(width=5, textvariable=null_filter)
entry4 = Entry(width=5, textvariable=cut_off)

entry1.grid(column=0, row=1)
entry2.grid(column=0, row=4)
entry3.grid(column=0, row=6)
entry4.grid(column=2, row=1)


def get_file_path():
    get_file_path.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry1.delete(0, END)
    entry1.insert(0, get_file_path.file_path)


def trim_msa():
    file = open(get_file_path.file_path)
    df = pd.read_csv(file, encoding='utf-8', header=None)
    df = df.drop(df.columns[[0]], axis=1)
    label = label_number.get() - 1
    df = df.rename(columns=lambda x: x + label)
    df = df.replace({'-': None})
    index_len = len(df.index)
    null_val = null_filter.get()

    for i in df:
        non_nulls = df[i].count()
        info_amount = non_nulls / index_len
        print(info_amount)
        if info_amount < null_val:
            del df[i]

    df = df.rename(index={0: 'solved'})

    df = df.replace({None: '-'})  # must return inserts to str in order to run
    t.delete(1.0, END)
    t.insert(INSERT, df)


button1 = Button(text='Select File', fg='white', bg='purple', command=get_file_path)
button2 = Button(text='Trim MSA by Value', fg='white', bg='purple', command=trim_msa)
button3 = Button(text='Submit and Run', fg='purple', bg='yellow', command=window.destroy)

button1.grid(column=0, row=2)
button2.grid(column=0, row=7)
button3.grid(column=25, row=1)


# ----------- MSA-Processing Filter---------------------

window.mainloop()
