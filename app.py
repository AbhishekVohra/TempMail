import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, filedialog, Text, Frame, Button, Menu
from tkinter.scrolledtext import ScrolledText
import requests
import random
import string
import os
from bs4 import BeautifulSoup  # Make sure to install this package

# Base URL for 1secmail API
BASE_URL = 'https://www.1secmail.com/api/v1/'

class TempMailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temp Mail Application")
        self.root.geometry("1200x600")
        self.root.configure(bg='#2B2B2B')
        import ctypes

        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        # self.root.iconbitmap(r"D:/tempmail/icon.ico")
        self.root.after(201, lambda: root.iconbitmap('D:/tempmail/icon.ico'))

        self.emails = []
        self.attachments_info = {}

        self.setup_ui()

    def setup_ui(self):
        # Top frame for title
        self.top_frame = tk.Frame(self.root, bg='#2B2B2B')
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        # Title Label
        self.title_label = tk.Label(self.top_frame, text="Temp Mail", bg='#2B2B2B', fg='white', font=('Arial', 24, 'bold'))
        self.title_label.pack(pady=10)

        # Left frame for buttons and email list
        self.left_frame = tk.Frame(self.root, bg='#2B2B2B', padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Generate Email Button
        self.generate_button = tk.Button(self.left_frame, text="Generate Email", command=self.generate_email, bg='#00BCD4', fg='white', font=('Arial', 12, 'bold'))
        self.generate_button.pack(fill=tk.X, pady=5)

        # Check Inbox Button
        self.check_button = tk.Button(self.left_frame, text="Check Inbox", command=self.check_inbox, bg='#00BCD4', fg='white', font=('Arial', 12, 'bold'))
        self.check_button.pack(fill=tk.X, pady=5)

        # Email List Label
        self.email_list_label = tk.Label(self.left_frame, text="Previously Generated Emails:", bg='#2B2B2B', fg='white', font=('Arial', 12))
        self.email_list_label.pack(pady=10)

        # Email Listbox
        self.email_listbox_frame = tk.Frame(self.left_frame)
        self.email_listbox_frame.pack(fill=tk.BOTH, expand=True)
        self.email_listbox = Listbox(self.email_listbox_frame, width=30, height=20, font=('Arial', 12), bg='#424242', fg='white', selectbackground='#00BCD4')
        self.email_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for Listbox
        self.scrollbar = Scrollbar(self.email_listbox_frame, orient=tk.VERTICAL, command=self.email_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.email_listbox.config(yscrollcommand=self.scrollbar.set)

        # Bind right-click context menu
        self.email_listbox.bind("<Button-3>", self.show_context_menu)

        # Right frame for inbox and download buttons
        self.right_frame = tk.Frame(self.root, bg='#2B2B2B', padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Inbox Label
        self.inbox_label = tk.Label(self.right_frame, text="Inbox", bg='#2B2B2B', fg='white', font=('Arial', 16, 'bold'))
        self.inbox_label.pack(pady=5)

        # Inbox Frame
        self.inbox_frame = tk.Frame(self.right_frame, bg='#2B2B2B')
        self.inbox_frame.pack(expand=True, fill=tk.BOTH)

        self.inbox_canvas = tk.Canvas(self.inbox_frame, bg='#2B2B2B')
        self.inbox_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.inbox_scrollbar = tk.Scrollbar(self.inbox_frame, orient=tk.VERTICAL, command=self.inbox_canvas.yview)
        self.inbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.inbox_canvas.config(yscrollcommand=self.inbox_scrollbar.set)

        self.inbox_content_frame = tk.Frame(self.inbox_canvas, bg='#2B2B2B')
        self.inbox_canvas.create_window((0, 0), window=self.inbox_content_frame, anchor='nw')

        self.inbox_content_frame.bind("<Configure>", lambda e: self.inbox_canvas.configure(scrollregion=self.inbox_canvas.bbox("all")))

        self.inbox_widgets = []

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def generate_context_menu(self):
        self.context_menu = Menu(self.email_listbox, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_email)
        self.context_menu.add_command(label="Delete", command=self.delete_email)

    def copy_email(self):
        selected_email = self.email_listbox.get(tk.ACTIVE)
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_email)
        self.root.update()

    def delete_email(self):
        selected_email = self.email_listbox.get(tk.ACTIVE)
        self.email_listbox.delete(tk.ACTIVE)
        self.emails.remove(selected_email)
        with open('email_addresses.txt', 'w') as file:
            for email in self.emails:
                file.write(email + '\n')

    def generate_username(self, length=10):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

    def generate_temp_email(self):
        username = self.generate_username()
        domain = '1secmail.com'
        email = f"{username}@{domain}"
        return email

    def generate_email(self):
        email_address = self.generate_temp_email()
        self.emails.append(email_address)
        self.email_listbox.insert(tk.END, email_address)
        self.save_email(email_address)
        messagebox.showinfo("Generated Email", f"Temporary Email Address: {email_address}")

    def check_inbox(self):
        selected_email = self.email_listbox.get(tk.ACTIVE)
        if not selected_email:
            messagebox.showwarning("No Selection", "Please select an email address from the list.")
            return

        for widget in self.inbox_widgets:
            widget.destroy()
        self.inbox_widgets.clear()

        self.attachments_info.clear()

        username, domain = selected_email.split('@')
        params = {
            'action': 'getMessages',
            'login': username,
            'domain': domain
        }
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            emails = response.json()

            if emails:
                for mail in emails:
                    email_frame = tk.Frame(self.inbox_content_frame, bg='#2B2B2B', pady=5, height=100)
                    email_frame.pack(fill=tk.X)

                    email_text = ScrolledText(email_frame, font=('Arial', 12), bg='#424242', fg='white', wrap=tk.WORD, height=10)
                    email_text.insert(tk.END, f"From: {mail['from']}\n")
                    email_text.insert(tk.END, f"Subject: {mail['subject']}\n")
                    email_text.insert(tk.END, f"Date: {mail['date']}\n")

                    mail_id = mail['id']
                    mail_content = self.get_email_content(username, domain, mail_id)
                    if mail_content:
                        if mail_content.startswith('<'):
                            soup = BeautifulSoup(mail_content, 'html.parser')
                            email_text.insert(tk.END, f"Content: {soup.prettify()}\n")
                        else:
                            email_text.insert(tk.END, f"Content: {mail_content}\n")
                    email_text.config(state=tk.DISABLED)
                    email_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                    # Create download button for attachments
                    if mail_id in self.attachments_info:
                        button = Button(email_frame, text="Download Attachments", command=lambda m_id=mail_id: self.download_attachments(m_id), bg='#00BCD4', fg='white', font=('Arial', 12, 'bold'))
                        button.pack(side=tk.RIGHT, padx=5, pady=5)
                        self.inbox_widgets.append(button)

                    self.inbox_widgets.append(email_text)
                    self.inbox_widgets.append(email_frame)
            else:
                empty_label = tk.Label(self.inbox_content_frame, text="Inbox is empty.", bg='#2B2B2B', fg='white', font=('Arial', 12))
                empty_label.pack(pady=10)
                self.inbox_widgets.append(empty_label)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error checking inbox: {e}")

    def get_email_content(self, username, domain, mail_id):
        params = {
            'action': 'readMessage',
            'login': username,
            'domain': domain,
            'id': mail_id
        }
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            mail_content = response.json()
            text_body = mail_content.get('textBody') or mail_content.get('htmlBody') or 'No content available'
            attachments = mail_content.get('attachments')
            if attachments:
                attachment_str = "\nAttachments:\n" + "\n".join([att['filename'] for att in attachments])
                text_body += attachment_str
                self.attachments_info[mail_id] = attachments
            return text_body
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error reading email content: {e}")
            return None

    def download_attachments(self, mail_id):
        selected_email = self.email_listbox.get(tk.ACTIVE)
        if not selected_email:
            messagebox.showwarning("No Selection", "Please select an email address from the list.")
            return

        username, domain = selected_email.split('@')
        attachments = self.attachments_info.get(mail_id, [])
        save_path = filedialog.askdirectory()
        if not save_path:
            return

        for attachment in attachments:
            file_name = attachment['filename']
            download_url = f"{BASE_URL}/download/{username}/{domain}/{attachment['filename']}"
            try:
                response = requests.get(download_url)
                response.raise_for_status()
                with open(os.path.join(save_path, file_name), 'wb') as file:
                    file.write(response.content)
                messagebox.showinfo("Download Complete", f"Attachment {file_name} downloaded successfully.")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Error downloading attachment: {e}")

    def save_email(self, email):
        with open('email_addresses.txt', 'a') as file:
            file.write(email + '\n')

    def load_saved_emails(self):
        try:
            with open('email_addresses.txt', 'r') as file:
                emails = file.readlines()
            return [email.strip() for email in emails]
        except FileNotFoundError:
            return []

    def run(self):
        saved_emails = self.load_saved_emails()
        for email in saved_emails:
            self.email_listbox.insert(tk.END, email)
        self.generate_context_menu()
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TempMailApp(root)
    app.run()
