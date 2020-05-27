import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
import pandas as pd
import importlib
import time
import re

window = Tk()
window.title('K Modes Alpha H')
window.geometry('650x650')
old_stdout = sys.stdout


class RedirectStdIO(object):
    def __init__(self, text_ctrl):
        self.output = text_ctrl

    def write(self, string):
        self.output.update_idletasks()
        self.output.delete(1.0, END)
        self.output.insert(tkinter.END, string)


# style macros
b_color = 'light gray'
f_color = 'black'

window.configure(bg=b_color)
window.resizable(False, False)

label1 = Label(window, text='\nSelect a CSV file for upload:' + '\n', anchor=CENTER, bg=b_color, fg=f_color)
label2 = Label(window, text='\nPercentage of information present in each column:', anchor=CENTER, bg=b_color, fg=f_color)
label3 = Label(window, text='\nEnter label number for actual sequence location of first column, '
                            'or automatically label based on first row', anchor=CENTER, bg=b_color, fg=f_color)

# Stderr Text Redirect
t = Text(window, height=18, width=85, bg='white', fg='black')
t.grid(column=2, row=7, padx=20)
redirect = RedirectStdIO(t)
sys.stdout = redirect
sys.stderr = redirect

sys.stdout.write("Welcome to K Modes Alpha!\n"
                 "\n(1) Please choose an MSA to run."
                 "\n(2) You may choose 'Preprocess-MSA' to filter high insertion sites."
                 "\n(3) Label your columns according to your preference."
                 "\n(4) When ready, press 'Submit and Run' to begin."
                 "\n\n\nPlease send error reports to ttownsley@mail.lipscomb.edu ")

f1 = Frame(window)
f1.grid(column=2, row=1)

f2 = Frame(window)
f2.grid(column=2, row=6, pady=16)

f3 = Frame(window)
f3.grid(row=8, column=2, pady=20)

label1.grid(column=2, row=0)
label2.grid(column=2, row=3)
label3.grid(column=2, row=5)

check_yes = IntVar()
check_box = Checkbutton(f2, variable=check_yes, text="Label using 1st row", bg=b_color, fg='purple')
check_box.pack(side="right")

label_number = IntVar()
label_number.set(1)
cut_off = DoubleVar()
cut_off.set(.15)
null_filter = StringVar()
null_filter.set("20%")

entry1 = Entry(f1, width=30)
entry2 = Entry(f2, width=3, textvariable=label_number)
entry3 = Entry(width=5, textvariable=null_filter)

entry1.pack(side="left")
entry2.pack(side="left")
entry3.grid(column=2, row=4, pady=6)


def get_file_path():
    get_file_path.file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry1.delete(0, END)
    entry1.insert(0, get_file_path.file_path)


def trim_msa():
    file = open(get_file_path.file_path)
    trim_msa.df = pd.read_csv(file, encoding='utf-8', header=None)

    def deweese_schema(df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns={df.columns[0]: 'SEQUENCE_ID'})
        df = df.set_index('SEQUENCE_ID', drop=True)
        df = df.rename(columns=lambda x: x - 1)
        first_row_ix = df.index[0]
        ix_label = first_row_ix.rsplit('/', 1)
        ix_label = ix_label[1]
        ix_label = ix_label.rsplit('-', 1)
        df_label = int(ix_label[0])
        column_lab_dict = dict()

        pattern = '^-'
        for i in df:
            if not re.search(pattern, df[i].iloc[0]):
                column_lab_dict[df.columns[i]] = df_label
                df_label += 1
            else:
                column_lab_dict[df.columns[i]] = ''
        df = df.rename(columns=column_lab_dict)
        df = df.drop(columns=[''])
        df = df.rename(columns=lambda x: int(x))

        return df

    def durston_schema(df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns={df.columns[0]: 'SEQUENCE_ID'})
        df = df.set_index('SEQUENCE_ID', drop=True)
        df.columns = range(len(df.columns))
        label_val = label_number.get()
        df = df.rename(columns=lambda x: int(x) + label_val)

        return df

    if check_yes.get() == 1:
        trim_msa.df = deweese_schema(trim_msa.df)

    # Remove High Insertion Areas
    trim_msa.df = trim_msa.df.replace({'-': None})
    index_len = len(trim_msa.df.index)
    null_val = float(null_filter.get().split("%")[0]) / 100
    for label, column in trim_msa.df.items():
        non_nulls = column.count()
        info_amount = non_nulls / index_len
        if info_amount < null_val:
            trim_msa.df = trim_msa.df.drop(columns=[label])
    trim_msa.df = trim_msa.df.replace({None: '-'})  # must return 'None' inserts to '-' str in order to run

    if check_yes.get() == 0:
        trim_msa.df = durston_schema(trim_msa.df)

    t.delete(1.0, END)
    t.insert(INSERT, trim_msa.df)
    button3.config(state='normal', bg='green')


def submit_and_run():
    submit_and_run.df = trim_msa.df
    path = 'preprocessed_msa.csv'
    sys.stdout.write("Writing preprocessed MSA to file...")
    submit_and_run.df.to_csv(path, index=True, header=True)
    importlib.import_module('src.kmodes_alpha_h')
    importlib.import_module('src.preprocessor')
    window.destroy()


button1 = Button(f1, text='Select File', fg='white', bg='purple', command=get_file_path)
button2 = Button(f3, text='Pre-Process MSA', fg='white', bg='purple', command=trim_msa)
button3 = Button(f3, text='Submit and Run', fg='white', bg='grey', command=submit_and_run)
button3.config(state='disabled')
button1.pack(side="right")
button2.pack(side="left")
button3.pack(side="right")


window.mainloop()
