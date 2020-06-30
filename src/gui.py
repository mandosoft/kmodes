import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.font as tkfont
import pandas as pd
import importlib
import re


old_stdout = sys.stdout


class RedirectStdIO(object):
    def __init__(self, text_ctrl):
        self.output = text_ctrl

    def write(self, string):
        self.output.update_idletasks()
        self.output.delete(1.0, END)
        self.output.insert(tkinter.END, string)


class Window(Tk):
    """
    Window for helper gui
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "K Modes Alpha")
        b_color = 'light gray'
        f_color = 'black'
        self.file_path = None
        self.df = None
        self.cut_off = DoubleVar()
        self.cut_off.set(.15)

        """Entry Area 1"""
        label1 = Label(self, text='\nSelect a CSV file for upload:' + '\n', anchor=CENTER)
        label1.pack(side="top", pady=(20, 5))
        f1 = Frame(self)
        self.entry1 = Entry(f1, width=30)
        button1 = Button(f1, text='Load MSA', fg='white', bg='MediumPurple3', command=self.get_file_path)
        button4 = Button(f1, text='Load Tree File', fg='white', bg='deep sky blue', command=self.load_tree_data)
        button4.pack(side="right")
        button1.pack(side="right")
        self.entry1.pack(side="top", fill=NONE, expand=True)
        f1.pack(side="top", fill=NONE, expand=False)

        """Entry Area 2"""
        label2 = Label(self, text='\nPercentage of information present in each column:', anchor=CENTER)
        label2.pack(side="top", pady=(10, 5))
        f2 = Frame(self)
        self.null_filter = StringVar()
        self.null_filter.set("20%")
        self.entry3 = Entry(width=5, textvariable=self.null_filter)
        self.entry3.pack(side="top")

        f2.pack(side="top")

        """Entry Area 3"""
        label3 = Label(self, text='\nEnter label number for actual sequence location of first column, '
                                  'or automatically label based on first row', anchor=CENTER)
        label3.pack(side="top", pady=(10, 5))
        f3 = Frame(self)
        self.check_yes = IntVar()
        check_box = Checkbutton(f3, variable=self.check_yes, text="Label using 1st row", bg=b_color, fg='purple')
        check_box.pack(side="right")
        self.label_number = IntVar()
        self.label_number.set(1)
        self.entry2 = Entry(f3, width=3, textvariable=self.label_number)
        self.entry2.pack(side="top")

        f3.pack(side="top", pady=(10, 5))

        """Text Window Area"""
        self.dataframe_manager = TextFrame()
        self.dataframe_manager.pack(side="top", fill=BOTH, expand=True, pady=(10, 5))

        """Submit Buttons Area"""
        f4 = Frame(self)
        button2 = Button(f4, text='Pre-Process MSA', fg='white', bg='MediumPurple3', command=self.preprocess_msa)
        self.button3 = Button(f4, text='Submit and Run', fg='white', bg='grey', command=self.submit_and_run)
        button2.pack(side="left")
        self.button3.pack(side="right")
        self.button3.config(state='disabled')

        f4.pack(side="top", pady=(10, 30))

    def get_file_path(self):
        global tree_path
        self.file_path = askopenfilename(filetypes=[("CSV files", "*.csv"), ("Fasta files", "*.txt")])
        self.entry1.delete(0, END)
        self.entry1.insert(0, self.file_path)
        tree_path = None

        return tree_path

    def load_tree_data(self):
        global tree_path
        self.file_path = askopenfilename(filetypes=[("CSV files", "*.csv"), ("Fasta files", "*.txt")])
        tree_path = self.file_path

        return tree_path, app.destroy()

    def preprocess_msa(self):

        if self.dataframe_manager.text['font'] != "TkFixedFont":
            self.dataframe_manager.text['font'] = "TkFixedFont"

        file = open(self.file_path)

        if str(self.file_path).endswith(".txt"):

            nucs_dict = dict()

            with open(self.file_path, "r") as a_file:
                string_without_line_breaks = ""
                for line in a_file:
                    stripped_line = line.rstrip()
                    string_without_line_breaks += stripped_line
                a_file.close()

            vals = string_without_line_breaks.split('>')
            for line in vals:
                line = re.split('(\w+/\d*-?\d*)', line)
                line.remove('')
                for i in enumerate(line):
                    g = list(line[1])
                    nucs_dict.update({line[0]: g})

            df = pd.DataFrame.from_dict(nucs_dict, orient='index')

        else:
            df = pd.read_csv(file, encoding='utf-8', engine='c', header=None)

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
            label_val = self.label_number.get()
            df = df.rename(columns=lambda x: int(x) + label_val)

            return df

        if self.check_yes.get() == 1:
            df = deweese_schema(df)

        # Remove High Insertion Areas
        df = df.replace({'-': None})
        index_len = len(df.index)
        null_val = float(self.null_filter.get().split("%")[0]) / 100

        for label, column in df.items():
            non_nulls = column.count()
            info_amount = non_nulls / index_len
            if info_amount < null_val:
                df = df.drop(columns=[label])
        df = df.replace({None: '-'})  # must return 'None' inserts to '-' str in order to run

        if self.check_yes.get() == 0:
            df = durston_schema(df)

        self.dataframe_manager.text.delete(1.0, END)
        self.dataframe_manager.text.insert(INSERT, df)
        self.df = df
        self.button3.config(state='normal', bg='SeaGreen3')

    def submit_and_run(self):
        self.dataframe_manager.text['font'] = tkfont.Font(size=10)
        global submitted_df
        submitted_df = self.df
        path = 'preprocessed_msa.csv'
        sys.stdout.write("Writing preprocessed MSA to file...")
        submitted_df.to_csv(path, index=True, header=True)
        importlib.import_module('src.kmodes_alpha_h')
        importlib.import_module('src.preprocessor')

        return app.destroy()


class TextFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.dialog_font = tkfont.Font(size=10)
        self.text = Text(self, height=18, width=85, bg='white', fg='black', font=self.dialog_font)
        self.text.pack(side=TOP, fill=BOTH, expand=True, anchor=CENTER, padx=20)

        redirect = RedirectStdIO(self.text)
        #sys.stdout = redirect
        #sys.stderr = redirect

        sys.stdout.write("Welcome to K Modes Alpha!\n"
                         "\n(1) Please choose an MSA to run."
                         "\n(2) You may choose 'Preprocess-MSA' to filter high insertion sites."
                         "\n(3) Label your columns according to your preference."
                         "\n(4) When ready, press 'Submit and Run' to begin."
                         "\n\n\nPlease send error reports to ttownsley@mail.lipscomb.edu ")


app = Window()
app.geometry('650x650')
app.protocol("WM_DELETE_WINDOW", exit)
app.mainloop()
