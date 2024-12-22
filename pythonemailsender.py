import sys
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

class MailSender(QWidget):
    def __init__(self): 
        super().__init__()

        self.init_ui()

    def init_ui(self):

        self.setWindowTitle('Python Email Sender')
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #F4F4F9;")
        
        layout = QVBoxLayout()

        self.recipient_label = QLabel('Recipient Email:')
        self.recipient_label.setStyleSheet("font-size: 25px; color: #000000;")
        self.recipient_input = QLineEdit(self)
        self.recipient_input.setPlaceholderText('Enter recipient email address')
        self.recipient_input.setStyleSheet("padding: 8px; border: 1px solid #ddd; border-radius: 5px;")

        self.subject_label = QLabel('Subject:')
        self.subject_label.setStyleSheet("font-size: 25px; color: #000000;")
        self.subject_input = QLineEdit(self)
        self.subject_input.setPlaceholderText('Enter email subject')
        self.subject_input.setStyleSheet("padding: 8px; border: 1px solid #ddd; border-radius: 5px;")

        self.message_label = QLabel('Message Body:')
        self.message_label.setStyleSheet("font-size: 25px; color: #000000;")
        self.message_input = QTextEdit(self)
        self.message_input.setPlaceholderText('Type your message here...')
        self.message_input.setStyleSheet("padding: 8px; border: 1px solid #ddd; border-radius: 5px; min-height: 150px;")

        self.attachment_button = QPushButton('Add Attachment')
        self.attachment_button.setStyleSheet("""
            QPushButton {
                background-color: #0000FF;
                color: white;
                border: none;
                padding: 15px 32px;
                font-size: 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #000000;
                cursor: pointer;
            }
        """)
        self.attachment_button.clicked.connect(self.attach_file)

        # Send Button
        self.send_button = QPushButton('Send Email')
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 32px;
                font-size: 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #000000;
                cursor: pointer;
            }
        """)
        self.send_button.clicked.connect(self.send_email)

        


        layout.addWidget(self.recipient_label)
        layout.addWidget(self.recipient_input)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_input)
        layout.addWidget(self.attachment_button)
        layout.addWidget(self.send_button)

        self.notification_label = QLabel("")
        self.notification_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.notification_label)


        self.setLayout(layout)

        self.attachment_file = None  

    def attach_file(self):
   
        self.attachment_file, _ = QFileDialog.getOpenFileName(self, 'Select Attachment', '', 'All Files (*);;JPEG Files (*.jpg *.jpeg);;PNG Files (*.png)')

    def send_email(self):
        recipient = self.recipient_input.text()
        subject = self.subject_input.text()
        message = self.message_input.toPlainText()

        if not recipient or not subject or not message:
            print("All fields are required")
            return

        try:
          
            with open('password.txt', 'r') as f: #Create a file named: password.txt storing your gmail account password in your project directory 
                password = f.read()

           
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login('Senders Email', password)

    
            msg = MIMEMultipart()
            msg['From'] = 'Senders Name'
            msg['To'] = recipient
            msg['Subject'] = subject

         
            msg.attach(MIMEText(message, 'plain'))

          
            if self.attachment_file:
                filename = self.attachment_file.split('/')[-1]
                with open(self.attachment_file, 'rb') as attachment:
                    p = MIMEBase('application', 'octet-stream')
                    p.set_payload(attachment.read())
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', f'attachment; filename={filename}')
                    msg.attach(p)

            # Send the email
            text = msg.as_string()
            server.sendmail('Senders Email', recipient, text)
            self.notification_label.setText("Email sent successfully!")
            self.notification_label.setStyleSheet("color: green; font-weight: bold;")

        except Exception as e:
            print(f"Error sending email: {e}")

        finally:
            server.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MailSender()
    window.show()
    sys.exit(app.exec_())
