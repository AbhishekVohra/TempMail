# TempMail Application

Welcome to the TempMail Application! This project provides a simple and efficient way to generate temporary email addresses, check their inboxes, and download any attachments. This application is built using Python and Tkinter for the GUI, and it uses the 1secmail API for generating and managing temporary emails.

## Features

- **Generate Temporary Email:** Easily generate a new temporary email address with the click of a button.
- **Check Inbox:** View the inbox of any generated email address and read received messages.
- **Download Attachments:** Download attachments from any email that contains them.
- **Custom Icon:** The application has a custom icon for both the window and the taskbar.
- **Standalone Executable:** Compile the application into a standalone executable for easy distribution.

## Getting Started

Follow these steps to set up and run the TempMail application on your local machine.

### Prerequisites

- Python 3.x
- `pip` (Python package installer)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/tempmail.git
   cd tempmail
   ```
2. **Running the Application:**

   ```
   python app.py
   ```

### Creating standalone Executable

Although the executable is already attached, but to create a standalone executable for your application, follow these steps:

1. **Install Pyinstaller**

   ```
   pip install pyinstaller
   ```
2. **Generate the Executable**

   ```
   pyinstaller --onefile --noconsole --icon=icon.ico app.py
   ```
3. **Locate the Executable**
   The executable will be created in the `dist` directory inside your project folder. You can run the application by double-clicking the `app.exe` file in the `dist` directory.


### Usage Instructions

1. **Generate Email:**
   * Click the "Generate Email" button to create a new temporary email address.
   * The generated email address will be displayed in the list of previously generated emails.
2. **Check Inbox:**
   * Select an email address from the list and click the "Check Inbox" button.
   * The inbox will be displayed on the right side of the application window.
3. **Download Attachments:**
   * If an email contains attachments, a "Download Attachments" button will be displayed next to the email content.
   * Click the button to download the attachments to a directory of your choice.

### Customizing the Application

To customize the application for your own use, you can:

1. **Change the Icon:**
   * Replace the `icon.ico` file with your own icon file.
   * Ensure the new icon file is in `.ico` format.
2. **Modify the User Interface:**
   * Edit the `app.py` file to change the layout, colors, or functionality of the application.

### Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.


### Acknowledgments

* This application uses the 1secmail API for generating and managing temporary emails.
* Special thanks to the developers of the libraries and tools used in this project.
