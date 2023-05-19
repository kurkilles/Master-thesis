from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import numpy as np
import main_program as mp

root = Tk()
root.title("Factoring algorithm solver")
root.geometry("405x100")
test2 = np.array([[1,1,0,0,0],[1,1,0,0,0],[0,1,1,0,0],[0,0,1,1,0],[0,0,0,1,1],[0,0,0,1,1]])
matrix = np.array([])
connected_components = []
size = 0
file_name_text = ''

def w_file():
    global matrix
    matrix = np.array([])
    global connected_components
    global size
    global control
    global file_name
    global file_name_text
    root.matrix_file = filedialog.askopenfilename(initialdir = os.path.join(os.getcwd(),"matrixes"), title = "Select a file", filetypes = (("txt files", "*.txt"),("all files","*.*")))
    file_name_text = os.path.basename(root.matrix_file)
    with open(root.matrix_file, "r") as file:
        lines = file.readlines()
        try:
            size = int(lines[0].replace("\n", ""))
        except:
            w_message = "Check if the size of the matrix is in the file"
            warnings = Label(root, text = w_message, width = 58, borderwidth = 5)
            warnings.grid(row=6, column=0 , columnspan=2, sticky=W)
            return

        for line in lines[1:]:
            try:
                vector = np.zeros((1,size))
                line = line.replace("\n","").split(",")
                first = int(line[0])
                second = int(line[1])
                if first == second:
                    w_message = "Vertex can not be connected to itself"
                    warnings = Label(root, text = w_message, width = 58, borderwidth = 5)
                    warnings.grid(row=6, column=0 , columnspan=2, sticky=W)
                    return
                vector[0, first-1]=1
                vector[0, second-1]=1
                if matrix.size > 0:
                    matrix = np.vstack([matrix, vector])
                else:
                    matrix = vector
            except:
                w_message = "Something went wrong. Check if the file is appropriate"
                warnings = Label(root, text = w_message, width = 58, borderwidth = 5)
                warnings.grid(row=6, column=0, columnspan=2, sticky=W)
                return

    root.geometry("520x260")
    cc_label = Label(root, text="Which vertices should be connected?")
    cc = Entry(root, width = 10, borderwidth = 5)
    file_name_label = Label(root, text="What should be the name of the results file?")
    file_name = Entry(root, width = 10, borderwidth = 5)

    cc_label.grid(row=3, column=0, pady=20)
    cc.grid(row=3, column=1, padx=10, ipadx=90, sticky=E)
    file_name_label.grid(row=4, column=0)
    file_name.grid(row=4, column=1, padx=10, ipadx=90, sticky=E)

    button_solve = Button(root, text="Solve", command=lambda: solve(cc.get(), file_name.get()), borderwidth=4)
    button_solve.grid(row=5, column=0, columnspan=2, pady=50, ipadx=20)

def check():
    global matrix
    chc = Toplevel()
    clbl = Label(chc, text=matrix)
    clbl.pack()


def solve(cc_text, name):
    global matrix
    global connected_components
    global size

    if not cc_text:
        w_message = "First you must enter the connected vertices"
        warnings = Label(root, text = w_message, width = 58, borderwidth = 5)
        warnings.grid(row=6, column=0, columnspan=2, sticky=W)
        return

    cc_text = cc_text.replace("\n","")
    if cc_text == "all":
        connected_components = [x+1 for x in range(size)]
    else:
        connected_components = cc_text.split(",")
        connected_components = [int(a) for a in connected_components.copy()]
    sol = mp.Solution(mp.Solution.convert(matrix), size)

    if name:
        with open(os.path.join(os.path.join(os.getcwd(),"results"), "{}.txt".format(name)), "w") as f:
            f.write(sol.solve(connected_components))
    else:
        with open(os.path.join(os.path.join(os.getcwd(),"results"), "result.txt"), "w") as f:
            f.write(sol.solve(connected_components))

    done = messagebox.showinfo("done", "{} is done".format(file_name_text))


button_file = Button(root, text="Use file to implement your graph", command=w_file)
button_check = Button(root, text="Check current graph", command=check)

button_file.grid(row=1, column=0, columnspan=2, ipadx=110, pady=5)
button_check.grid(row=2, column=0, columnspan=2, ipadx=143, pady=5)

root.mainloop()