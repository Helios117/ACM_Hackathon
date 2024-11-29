import tkinter as tk
from tkinter import messagebox
import database
import google.generativeai as genai
import api_key

genai.configure(api_key=api_key.key)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
questionslen = 5
questions = []

current_question = 0
score = 0

# Quiz window
def register_user():

    name = name_entry.get()
    age = age_entry.get()
    contact_number = contact_entry.get()

    if not name or not age or not contact_number:
        messagebox.showerror("Input Error", "Please fill all fields.")
        return
   
    if not age.isdigit():
        messagebox.showerror("Age Error", "Please enter a valid age (numeric values only).")
        return

    if len(contact_number) < 10 or not contact_number.isdigit():
        messagebox.showerror("Contact Error", "Please enter a valid contact number with at least 10 digits.")
        return
   
 
    messagebox.showinfo("Registration Success", f"User {name} registered successfully!\nAge: {age}\nContact: {contact_number}")

    database.init()
    database.insert([name, age, contact_number])
    print(database.view(name, age))
    print("Done")

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)

    global questions

    def next_question():
        global current_question, questionslen
        if current_question < questionslen:
            global questions
            question = model.generate_content("Generate a single new Question related to digital skill with no extra text of beginner level. Dont ask these, as its asked already: " + "\n".join(questions))
            question_label.config(text=question.text)
            questions += [question.text]
            answer_entry.delete(0, tk.END)  
        else:
            show_score()

    def check_answer():
        global current_question, score, questions
        user_answer = answer_entry.get().strip().lower()
        print(questions[-1])
        checker = model.generate_content("For question: "+questions[-1]+"\nCheck if answer: "+user_answer+"is correct. Only say 1 if correct even remotely, and 0 if completely incorrect with no other text.")
        valid = checker.text

        print(valid)

        if "1" in valid:
            score += 1
    
        current_question += 1
        next_question()

    def show_score():
        messagebox.showinfo("Quiz Completed", f"Your score: {score}/{len(questions)}")
        root.quit()  

    q = tk.Tk()
    q.title("Quiz Application")

    question_label = tk.Label(q, text="", font=("Arial", 16), width=200, height=4)
    question_label.pack(pady=20)

    answer_entry = tk.Entry(q, font=("Arial", 14), width=50)
    answer_entry.pack(pady=10)

    submit_button = tk.Button(q, text="Submit Answer", font=("Arial", 14), command=check_answer)
    submit_button.pack(pady=10)

    next_question()
    root.destroy()

# Main window
root = tk.Tk()
root.title("User Profile Registration")

label_name = tk.Label(root, text="Full Name")
label_name.pack(padx=10, pady=5)
name_entry = tk.Entry(root, width=30)
name_entry.pack(padx=10, pady=5)

label_age = tk.Label(root, text="Age")
label_age.pack(padx=10, pady=5)
age_entry = tk.Entry(root, width=30)
age_entry.pack(padx=10, pady=5)

label_contact = tk.Label(root, text="Contact Number")
label_contact.pack(padx=10, pady=5)
contact_entry = tk.Entry(root, width=30)
contact_entry.pack(padx=10, pady=5)

register_button = tk.Button(root, text="Sign Up", command=register_user)
register_button.pack(padx=10, pady=10)

root.mainloop()