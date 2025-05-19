# 🎯 The Project Goal:
This project demonstrates the use of Apache Airflow with Docker, including a customized exchange rate (EUR/TWD) email alert based on data retrieved from Bank Sinopac (Taiwan) website.


# 🐍 Set up a Python Virtual Environment
```
python3 -m venv venv
source venv/bin/activate  # Mac/Linux, venv\Scripts\activate # Windows
pip install -r requirements.txt
```

# 🐳 Run Airflow in Docker
I was following this [doc](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).
Here shows the steps to set up and run Apache Airflow in a Docker environment.

## 1. Check System Memory
Ensure your system has at least 4 GB of memory:

```
docker run --rm "debian:bookworm-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'
```
P.S. It will create a debian:bookworm-slim image, you can safely delete it if you don't plan to use it again.

## 2. Create Required Folders
```
mkdir -p ./dags ./logs ./plugins ./config
```

## 3. Set Up Environment File
```
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
It will create a .env file with your system UID.


## 4. Initialize the Database
```
docker compose up airflow-init
```

## 5. Clean Up (Optional)
To clean up volumes and orphan containers:
```
docker compose down --volumes --remove-orphans
```

## 6. Configure Gmail SMTP settings in the service.conf
```
email.from = xxx # Please replace the email address with your own, as the my current configuration uses the same address for both the sender and the recipient
pass = xxx # You need to set up an App Password in your Gmail account to enable authentication for email sending
```
Note: You must first enable 2-Step Verification in your Google account. Once enabled, you can generate an App Password via [the following link](https://myaccount.google.com/apppasswords)


## 7. Start All Services
Start all Airflow services:

```
docker compose up
```

## Note:
 The default username is `airflow` and the default password is also `airflow`