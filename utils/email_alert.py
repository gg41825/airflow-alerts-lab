from email.mime.text import MIMEText
import smtplib
import config as config

def send_rate_info_email(**kwargs):
    rate_info = kwargs["ti"].xcom_pull(key="rate_info", task_ids="get_rate")
    if not rate_info:
      raise ValueError("No rate_info found in context")
    
    currency = rate_info["code"]
    buy_rate = rate_info["buy_rate"]
    sell_rate = rate_info["sell_rate"]
    middle_rate = (float(buy_rate) + float(sell_rate)) / 2

    user = config.config.get('gmail', 'email.from')
    password = config.config.get('gmail', 'pass')

    message = MIMEText(f'{currency}, Buy: {buy_rate}, Sell: {sell_rate}, Middle Rate: {middle_rate}', "plain", "utf-8")
    message["Subject"] = "Daily EUR/TWD Currentcy Rate Reminder"
    message["From"] = user
    message["To"] = user

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(user, password)
            server.send_message(message)
            print("Email sent successfully")
    except Exception as e:
        print("Error while sending email:", e)
    return "Email sent"