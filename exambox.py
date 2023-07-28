import tkinter as tk
from tkinter import filedialog, messagebox
import json


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('Quiz Application')
        self.root.geometry('800x600+200+200')
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Import', command=self.open_import_window)
        self.file_menu.add_command(label='List', command=self.open_question_list_window)
        self.file_menu.add_command(label='Quiz', command=self.open_quiz_window)


        self.question_list = []
        with open("D:\WorkStudio\PycharmProjects\pythonProject1\question.json", 'r', encoding="utf8") as f:
            data = json.load(f)
            self.question_list.extend(data)


    def open_quiz_window(self):
        QuizWindow(self)
    def open_import_window(self):
        ImportWindow(self)

    def open_question_list_window(self):
        QuestionListWindow(self)


class ImportWindow:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.question_list = []
        filename = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
        print(filename)
        if filename:
            with open(filename, 'r', encoding="utf8") as f:
                data = json.load(f)
                self.main_window.question_list.extend(data)
                messagebox.showinfo("Success", "Questions imported successfully!")
                # self.main_window.list_window.refresh_question()  # Add this line

class QuestionListWindow:
    def __init__(self, main_window):

        self.main_window = main_window

        self.window = tk.Toplevel()
        self.window.geometry('800x600')
        self.listbox = tk.Listbox(self.window)
        self.listbox.pack(fill=tk.BOTH, expand=1)

        for question in self.main_window.question_list:
            self.listbox.insert(tk.END, question['question'],"check")

        # quiz_button = tk.Button(self.window, text='check Selected Question', command=self.start_quiz)
        # quiz_button.pack()

        quiz_button = tk.Button(self.window, text='Add Question', command=self.add_question)
        quiz_button.pack()

    def start_quiz(self):
        selected_index = self.listbox.curselection()[0]
        selected_question = self.main_window.question_list[selected_index]
        # frame1 = tk.Frame(root, padx=10, pady=10, bg="lightblue")
        # frame1.pack(side=tk.LEFT, padx=20, pady=20)
        # QuizWindow(frame1,selected_question)




class QuestionWindow:
    def __init__(self, root, data):

        self.root = root

        self.question = data['question']
        self.choices = data['options']
        self.correct_answer = data['correct_option']
        self.explanation = data['explanation']
        self.vars = [tk.IntVar() for _ in self.choices]
        self.result_label = tk.Label(root)
        self.setup()

    def setup(self):
        # self.root.title('Multiple Choice Quiz')

        question_label = tk.Label(self.root, text=self.question)
        question_label.pack()

        for i, choice in enumerate(self.choices):
            c = tk.Checkbutton(self.root, text=self.choices[choice], variable=self.vars[i])
            c.pack()

        submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        submit_button.pack()

        self.result_label.pack()

    def submit(self):
        answers = [choice for var, choice in zip(self.vars, self.choices) if var.get()]
        print(answers[0])
        print(self.correct_answer)
        if answers[0] == self.correct_answer:
            self.result_label.config(text=f"Correct! \nExplanation: {self.explanation}",fg="green")
        else:
            self.result_label.config(text=f"Incorrect! Try again. \nExplanation: {self.explanation}",fg="red")



class QuizWindow:
    def __init__(self,main_window):
        self.main_window = main_window
        self.window = tk.Toplevel()
        self.window.geometry('800x600')
        self.question_label = tk.Label(self.window, text='', wraplength=800)
        self.question_label.pack()
        print(len(main_window.question_list))
        self.current_question_index = 0
        self.question_lists_len = len(main_window.question_list) - 1


        self.frame1 = tk.Frame(self.window, padx=10, pady=10, bg="lightblue")
        self.frame1.pack(side=tk.LEFT, padx=20, pady=20)

        next_button = tk.Button(self.window, text='Next Question', command=self.next_question)
        next_button.pack()

        previous_button = tk.Button(self.window, text='Previous Question', command=self.previous_question)
        previous_button.pack()

        self.refresh_question()

    def next_question(self):
        """
        still can change in the future, which makes disapear when == 0
        :return:
        """
        if self.current_question_index < self.question_lists_len:
            self.current_question_index += 1
            self.refresh_question()

    def previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.refresh_question()

    def refresh_question(self):
        current_question = self.main_window.question_list[self.current_question_index]['question']
        self.question_label.config(text=current_question)

        for widget in self.frame1.winfo_children():
            widget.destroy()
        QuestionWindow(self.frame1, self.main_window.question_list[self.current_question_index])

class MultipleChoiceApp:
    def __init__(self, root, data):

        self.root = root
        self.question = data['question']
        self.choices = data['choices']
        self.correct_answer = data['correct_answer']
        self.explanation = data['explanation']
        self.vars = [tk.IntVar() for _ in self.choices]
        self.result_label = tk.Label(root)
        self.setup()

    def setup(self):
        self.root.title('Multiple Choice Quiz')

        question_label = tk.Label(self.root, text=self.question)
        question_label.pack()

        for i, choice in enumerate(self.choices):
            c = tk.Checkbutton(self.root, text=choice, variable=self.vars[i])
            c.pack()

        submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        submit_button.pack()

        self.result_label.pack()

    def submit(self):
        answers = [choice for var, choice in zip(self.vars, self.choices) if var.get()]

        if answers == self.correct_answer:
            self.result_label.config(text=f"Correct! \nExplanation: {self.explanation}")
        else:
            self.result_label.config(text=f"Incorrect! Try again. \nExplanation: {self.explanation}")

# Read data from JSON file
# with open('question.json', 'r') as f:
#     data = json.load(f)

root = tk.Tk()
root.geometry('800x600+600+200')
app = MainWindow(root)
root.mainloop()
