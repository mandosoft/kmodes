from tkinter import *
from tkinter import filedialog
import pandas as pd
import importlib
import time
import runpy

window = Tk()
window.title('K Modes Alpha H')
window.geometry('2500x1500')

# style macros
b_color = '#3e434a'
f_color = 'white'

window.configure(bg=b_color)

label1 = Label(window, text='\nSelect a CSV file for upload:' + '\n'*4, anchor=CENTER, bg=b_color, fg=f_color)

label2 = Label(window, text='\n\nSet what percentage of information      \n'
                            'must be present in each column:\n', anchor=CENTER, padx=15,
               bg=b_color, fg=f_color)

label3 = Label(window, text='Enter label number for first aligned attribute\n (the actual sequence location '
                            'of the first aligned column)', anchor=CENTER, pady=100, bg=b_color, fg=f_color)

label4 = Label(window, text='\nSet Sr(mode) cutoff value.\nRecommended start value is 0.15:'
               , anchor=CENTER, bg=b_color, fg=f_color)

t = Text(window, height=18, width=85, bg='black', fg='white')
t.grid(column=2, row=7)

label1.grid(column=0, row=0)
label2.grid(column=0, row=3)
label3.grid(column=2, row=3)
label4.grid(column=2, row=0)

# progress = Progressbar(window, orient=HORIZONTAL, length=100, mode='determinate')
# progress.grid(column=0, row=1)


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

entry1.grid(column=0, row=0)
entry2.grid(column=2, row=4, pady=50)
entry3.grid(column=0, row=4)
entry4.grid(column=2, row=1)


def get_file_path():
    get_file_path.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry1.delete(0, END)
    entry1.insert(0, get_file_path.file_path)


def trim_msa():
    file = open(get_file_path.file_path)
    trim_msa.df = pd.read_csv(file, encoding='utf-8', header=None)
    trim_msa.df = trim_msa.df.replace({'-': None})

    index_len = len(trim_msa.df.index)
    null_val = null_filter.get()

    for i in trim_msa.df:
        non_nulls = trim_msa.df[i].count()
        info_amount = non_nulls / index_len
        if info_amount < null_val:
            del trim_msa.df[i]

    trim_msa.df = trim_msa.df.replace({None: '-'})  # must return 'None' inserts to '-' str in order to run
    trim_msa.df.columns = range(len(trim_msa.df.columns))
    label = label_number.get() - 1
    trim_msa.df = trim_msa.df.rename(columns=lambda x: x + label)
    trim_msa.df = trim_msa.df.rename(columns={trim_msa.df.columns[0]: 'SEQUENCE_ID'})
    t.delete(1.0, END)
    t.insert(INSERT, trim_msa.df)
    button3.config(state='normal', bg='green')


def submit_and_run():

    submit_and_run.df = trim_msa.df
    submit_and_run.df = submit_and_run.df.drop(submit_and_run.df.columns[[0]], axis=1)
    start_time = time.perf_counter()
    runpy.run_module('kmodes_alpha_h')
    runpy.run_module('preprocessor')
    total_time = round((time.perf_counter() - start_time), 3)
    runpy.run_module('tree_assembler')
    time_out = 'Took', total_time, 'seconds'
    t.delete(1.0, END)
    t.insert(INSERT, time_out)


button1 = Button(text='Select File', fg='white', bg='purple', command=get_file_path)
button2 = Button(text='Pre-Process MSA', fg='white', bg='purple', command=trim_msa)
button3 = Button(text='Submit and Run', fg='white', bg='grey', command=submit_and_run)
button3.config(state='disabled')

button1.grid(column=0, row=1)
button2.grid(column=2, row=20, pady=20)
button3.grid(column=3, row=0)


window.mainloop()
