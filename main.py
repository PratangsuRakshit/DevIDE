from pygments import highlight
from pygments.lexers.python import Python3Lexer
from pygments.formatters.html import HtmlFormatter
from pygments.formatters.latex import LatexFormatter
from pygments.formatters.bbcode import BBCodeFormatter
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

compiler = Tk()
compiler.title('DevIDE')
file_path = ''

editor = Text(undo=True)
editor.pack()

code_output = Text(height=10)
code_output.pack()

def cut():
    editor.event_generate(("<<Cut>>"))

def copy():
    editor.event_generate(("<<Copy>>"))

def paste():
    editor.event_generate(("<<Paste>>"))

def HTML():
    if repeat.get() == 0:
        code_output.delete('1.0', END)
    code_output.insert('1.0', highlight(editor.get('1.0', END), Python3Lexer(), HtmlFormatter()))

def Latex():
    if repeat.get() == 0:
        code_output.delete('1.0', END)
    code_output.insert('1.0', highlight(editor.get('1.0', END), Python3Lexer(), LatexFormatter()))

def set_file_path(path):
    global file_path
    file_path = path


def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)


def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)


def run():
    save_as()
    if repeat.get() == 0:
        code_output.delete('1.0', END)
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.insert('1.0', output)
    code_output.insert('1.0',  error)


menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Exit', command=exit)
file_menu.add_separator()
file_menu.add_command(label='Undo', command=editor.edit_undo)
file_menu.add_command(label='Redo', command=editor.edit_redo)
menu_bar.add_cascade(label='File', menu=file_menu)

repeat = IntVar()
run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
run_bar.add_checkbutton(label='Repeat', variable=repeat)
menu_bar.add_cascade(label='Run', menu=run_bar)

edit_bar = Menu(menu_bar, tearoff=0)
edit_bar.add_command(label='Cut', command=cut)
edit_bar.add_command(label='Copy', command=copy)
edit_bar.add_command(label='Paste', command=paste)
edit_bar.add_separator()
edit_bar.add_command(label='HTMLify', command=HTML)
edit_bar.add_command(label='Latexify', command=Latex)
menu_bar.add_cascade(label='Edit', menu=edit_bar)

compiler.config(menu=menu_bar)

compiler.mainloop()
