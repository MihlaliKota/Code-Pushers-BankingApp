import tkinter as tk
from time import gmtime, strftime
from tkinter import messagebox
import string
import random
import os

class TinkaBankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tinka Bank")
        self.configure(background='#29c5f6')
        self.frames = {}
        self.create_frames()
        self.show_frame("MainMenu")

    def create_frames(self):
        for F in (MainMenu, Login, CreateAccount, LoggedInMenu, DepositAmount, WithdrawAmount, TransactionHistory):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(background='#29c5f6')

        logo_image = tk.PhotoImage(file="918b31fa5a4b49a982796ff43e74db92 (1).png")
        logo_label = tk.Label(self, image=logo_image, bg='#29c5f6')
        logo_label.image = logo_image
        logo_label.pack(pady=10)

        fr_buttons = tk.Frame(self, bg="#29c5f6")
        fr_buttons.pack(pady=20)

        imgc = tk.PhotoImage(file="new.gif.png").subsample(2, 2)
        imglog = tk.PhotoImage(file="login.gif.png").subsample(2, 2)

        b1 = tk.Button(fr_buttons, image=imgc, command=lambda: controller.show_frame("CreateAccount"))
        b1.image = imgc
        b2 = tk.Button(fr_buttons, image=imglog, command=lambda: controller.show_frame("Login"))
        b2.image = imglog

        b1.grid(row=0, column=0, padx=20)
        b2.grid(row=0, column=1, padx=20)

        clock_label = tk.Label(self, font=("Courier", 20), fg="white", bg="black")
        clock_label.pack(pady=10)
        ClockUpdater(clock_label).update_clock()

class Login(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#29c5f6")

        l_title = tk.Message(self, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white",
                             bg="black", justify="center", anchor="center")
        l_title.config(font=("Courier", "50", "bold"))
        l_title.pack(side="top", pady=(5, 10))

        l1 = tk.Label(self, text="Enter Name:", relief="raised")
        l1.pack(side="top", pady=(8, 4))
        self.e1 = tk.Entry(self)
        self.e1.pack(side="top", pady=(0, 5))

        l2 = tk.Label(self, text="Enter account number:", relief="raised")
        l2.pack(side="top", pady=(8, 4))
        self.e2 = tk.Entry(self)
        self.e2.pack(side="top", pady=(0, 5))

        l3 = tk.Label(self, text="Enter your Password:", relief="raised")
        l3.pack(side="top", pady=(8, 4))
        self.e3 = tk.Entry(self, show="*")
        self.e3.pack(side="top", pady=(0, 10))

        b = tk.Button(self, text="Submit", command=self.check_log_in)
        b.pack(side="top", pady=(5, 5))

        b1 = tk.Button(self, text="HOME", relief="raised", bg="black", fg="white", command=lambda: controller.show_frame("MainMenu"))
        b1.pack(side="top", pady=(8, 8))

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(side="top", pady=(8, 8))

    def check_log_in(self):
        name = self.e1.get().strip()
        acc_num = self.e2.get().strip()
        pin = self.e3.get().strip()
        if not check_acc_nmb(acc_num, pin):
            messagebox.showinfo("Error", "Invalid Credentials! Try Again!")
            self.controller.show_frame("MainMenu")
            return

        if is_number(name):
            messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
            self.controller.show_frame("MainMenu")
        else:
            self.controller.show_frame("LoggedInMenu")
            self.controller.frames["LoggedInMenu"].set_user_info(acc_num, name)

class CreateAccount(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#29c5f6")

        l_title = tk.Message(self, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white",
                             bg="black", justify="center", anchor="center")
        l_title.config(font=("Courier", "50", "bold"))
        l_title.pack(side="top", pady=(10, 20))

        l1 = tk.Label(self, text="Enter Name:", relief="raised")
        l1.pack(side="top", pady=(8, 4))
        self.e1 = tk.Entry(self)
        self.e1.pack(side="top", pady=(0, 5))

        l2 = tk.Label(self, text="Enter Opening Deposit:", relief="raised")
        l2.pack(side="top", pady=(8, 4))
        self.e2 = tk.Entry(self)
        self.e2.pack(side="top", pady=(0, 5))

        l3 = tk.Label(self, text="Enter Desired Password:", relief="raised")
        l3.pack(side="top", pady=(8, 4))
        self.e3 = tk.Entry(self, show="*")
        self.e3.pack(side="top", pady=(8, 8))

        generate_password_button = tk.Button(self, text="Generate Password",
                                             command=lambda: generate_and_display_password(self.e3))
        generate_password_button.pack(side="top", pady=(5, 5))

        show_password_button = tk.Button(self, text="Show Password", command=self.toggle_password_visibility)
        show_password_button.pack(side="top", pady=(5, 5))

        b = tk.Button(self, text="Submit", command=self.create_account)
        b.pack(side="top")
        self.bind("<Return>", lambda x: self.create_account())

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(side="top", pady=(8, 8))

    def toggle_password_visibility(self):
        if self.e3.cget('show') == '*':
            self.e3.config(show='')
            self.show_password_button.config(text='Hide Password')
        else:
            self.e3.config(show='*')
            self.show_password_button.config(text='Show Password')

    def create_account(self):
        name = self.e1.get().strip()
        oc = self.e2.get().strip()
        pin = self.e3.get().strip()
        acc_num = generate_account_number()
        if not name or not oc or not pin:
            messagebox.showerror("Error", "All fields are required")
            return

        if not is_number(oc):
            messagebox.showerror("Error", "Opening deposit must be a number")
            return

        with open("accounts.txt", "a") as file:
            file.write(f"{acc_num},{name},{oc},{pin}\n")

        with open(f"{acc_num}_transactions.txt", "w") as file:
            file.write(f"CREDIT: {oc}\n")  # Write opening deposit as a transaction entry

        messagebox.showinfo("Success", f"Account created successfully. Your account number is {acc_num}")
        self.controller.show_frame("MainMenu")

class LoggedInMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(background='#29c5f6')

        l_title = tk.Message(self, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white",
                             bg="black", justify="center", anchor="center")
        l_title.config(font=("Courier", "50", "bold"))
        l_title.pack(side="top")

        self.label = tk.Label(self, relief="raised", bg="black", fg="white", anchor="center", justify="center")
        self.label.pack(side="top")

        img2 = tk.PhotoImage(file="credit.gif.png")
        myimg2 = img2.subsample(2, 2)
        img3 = tk.PhotoImage(file="debit.gif.png")
        myimg3 = img3.subsample(2, 2)
        img4 = tk.PhotoImage(file="balance1.gif.png")
        myimg4 = img4.subsample(2, 2)
        img5 = tk.PhotoImage(file="transaction.gif.png")
        myimg5 = img5.subsample(2, 2)
        img6 = tk.PhotoImage(file="logout.gif.png")
        myimg6 = img6.subsample(2, 2)

        self.b2 = tk.Button(self, image=myimg2, command=lambda: self.deposit())
        self.b2.image = myimg2
        self.b3 = tk.Button(self, image=myimg3, command=lambda: self.withdraw())
        self.b3.image = myimg3
        self.b4 = tk.Button(self, image=myimg4, command=self.show_balance)
        self.b4.image = myimg4
        self.b5 = tk.Button(self, image=myimg5, command=lambda: self.show_transactions())
        self.b5.image = myimg5
        self.b6 = tk.Button(self, image=myimg6, command=self.logout)
        self.b6.image = myimg6

        self.b2.pack(side="top", padx=10)
        self.b3.pack(side="top", padx=10)
        self.b4.pack(side="top", padx=10)
        self.b5.pack(side="top", padx=10)
        self.b6.pack(side="top", padx=10)

    def deposit(self):
        self.controller.show_frame("DepositAmount")
        self.enable_back_button()

    def withdraw(self):
        self.controller.show_frame("WithdrawAmount")
        self.enable_back_button()

    def show_balance(self):
        balance = get_balance(self.accnt)
        messagebox.showinfo("Balance", f"Your Balance is Rs.{balance}")
        self.enable_back_button()

    def show_transactions(self):
        transactions = get_transaction_history(self.accnt)
        self.controller.frames["TransactionHistory"].update_history(transactions)
        self.controller.show_frame("TransactionHistory")
        self.enable_back_button()

    def logout(self):
        self.controller.show_frame("MainMenu")

    def set_user_info(self, accnt, name):
        self.accnt = accnt
        self.name = name
        self.label.config(text="Welcome {}. Your account number is {}".format(name, accnt))


class DepositAmount(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        l_title = tk.Message(self, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white",
                             bg="black", justify="center", anchor="center")
        l_title.config(font=("Courier", "50", "bold"))
        l_title.pack(side="top")

        l1 = tk.Label(self, text="Enter Amount to be deposited:", relief="raised")
        l1.pack(side="top", pady=(8, 4))
        self.e1 = tk.Entry(self)
        self.e1.pack(side="top", pady=(0, 5))

        b = tk.Button(self, text="Submit", command=self.deposit_amount)
        b.pack(side="top", pady=(5, 5))

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("LoggedInMenu"))
        back_button.pack(side="top", pady=(8, 8))

    def deposit_amount(self):
        amount = self.e1.get().strip()
        if not amount or not is_number(amount):
            messagebox.showerror("Error", "Please enter a valid amount")
            return

        write_to_file(self.controller.frames["LoggedInMenu"].accnt, "CREDIT", amount)
        messagebox.showinfo("Success", "Amount Deposited Successfully")
        self.controller.show_frame("LoggedInMenu")

class WithdrawAmount(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        l_title = tk.Message(self, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white",
                             bg="black", justify="center", anchor="center")
        l_title.config(font=("Courier", "50", "bold"))
        l_title.pack(side="top")

        l1 = tk.Label(self, text="Enter Amount to be withdrawn:", relief="raised")
        l1.pack(side="top", pady=(8, 4))
        self.e1 = tk.Entry(self)
        self.e1.pack(side="top", pady=(0, 5))

        b = tk.Button(self, text="Submit", command=self.withdraw_amount)
        b.pack(side="top", pady=(5, 5))

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("LoggedInMenu"))
        back_button.pack(side="top", pady=(8, 8))

    def withdraw_amount(self):
        amount = self.e1.get().strip()
        if not amount or not is_number(amount):
            messagebox.showerror("Error", "Please enter a valid amount")
            return

        balance = get_balance(self.controller.frames["LoggedInMenu"].accnt)
        if float(amount) > balance:
            messagebox.showerror("Error", "Insufficient balance")
            return

        write_to_file(self.controller.frames["LoggedInMenu"].accnt, "DEBIT", amount)
        messagebox.showinfo("Success", "Amount Withdrawn Successfully")
        self.controller.show_frame("LoggedInMenu")

class TransactionHistory(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        l_title = tk.Message(self, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white",
                             bg="black", justify="center", anchor="center")
        l_title.config(font=("Courier", "50", "bold"))
        l_title.pack(side="top")

        self.history_text = tk.Text(self)
        self.history_text.pack(side="top")

        b = tk.Button(self, text="Back", command=lambda: controller.show_frame("LoggedInMenu"))
        b.pack(side="top", pady=(5, 5))

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("LoggedInMenu"))
        back_button.pack(side="top", pady=(8, 8))

    def update_history(self, transactions):
        self.history_text.delete(1.0, tk.END)
        for transaction in transactions:
            self.history_text.insert(tk.END, transaction + "\n")

class ClockUpdater:
    def __init__(self, label):
        self.label = label

    def update_clock(self):
        current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.label.config(text=current_time)
        self.label.after(1000, self.update_clock)

def generate_and_display_password(entry):
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    entry.delete(0, tk.END)
    entry.insert(0, password)
    messagebox.showinfo("Generated Password", f"Your generated password is: {password}")

def write_to_file(acc_num, transaction_type, amount):
    with open(f"{acc_num}_transactions.txt", "a") as file:
        file.write(f"{transaction_type}: {amount}\n")

def check_acc_nmb(acc_num, pin):
    if not os.path.exists("accounts.txt"):
        return False
    with open("accounts.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if data[0] == acc_num and data[3] == pin:
                return True
    return False

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def generate_account_number():
    return ''.join(random.choices(string.digits, k=10))

def get_balance(acc_num):
    balance = 0.0
    with open(f"{acc_num}_transactions.txt", "r") as file:
        for line in file:
            if "CREDIT" in line:
                balance += float(line.split(":")[1].strip())
            elif "DEBIT" in line:
                balance -= float(line.split(":")[1].strip())
    return balance

def get_transaction_history(acc_num):
    transactions = []
    with open(f"{acc_num}_transactions.txt", "r") as file:
        transactions = file.readlines()
    return transactions

if __name__ == "__main__":
    app = TinkaBankApp()
    app.mainloop()
