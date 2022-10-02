def send_email(*args, **kwargs):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Function to send email here
    
    return 

def add_value_to_list_elements(num, value_list):
    return {
        "list": [value+1 for value in value_list], 
        "name": "somename"
        }

def print_completed():
    print("Completed !!")