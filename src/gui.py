from tkinter import *
from tkinter import filedialog

window = Tk()
window.title('K Modes Alpha H')
window.geometry('800x900')

label1 = Label(window, text='Select a CSV file for upload:', anchor=CENTER, pady=30)
label2 = Label(window, text='Enter label number for first aligned attribute\n (the actual sequence location '
                            'of the first aligned column):', anchor=CENTER, pady=30)
label3 = Label(window, text='\nSet Sr(mode) cutoff value.\nRecommended start value is 0.15.\n\n '
                            'Changing the value will increase or \n '
                            'decrease resolution of the tree:', anchor=CENTER, pady=30)

label1.grid(column=0, row=0)
label2.grid(column=0, row=3)
label3.grid(column=0, row=5)

label_number = IntVar()
label_number.set(1)
cut_off = DoubleVar()
cut_off.set(.15)
entry1 = Entry(width=30)
entry2 = Entry(width=3, textvariable=label_number)
entry3 = Entry(width=5, textvariable=cut_off)

entry1.grid(column=0, row=1, padx=15, pady=8)
entry2.grid(column=0, row=4)
entry3.grid(column=0, row=6)


def get_file_path():
    get_file_path.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry1.delete(0, END)
    entry1.insert(0, get_file_path.file_path)


button1 = Button(text='Select File', fg='white', bg='purple', command=get_file_path)
button2 = Button(text='Submit and Run', fg='white', bg='purple', command=window.destroy)

button1.grid(column=0, row=2)
button2.grid(column=0, row=10, pady=30)

window.mainloop()