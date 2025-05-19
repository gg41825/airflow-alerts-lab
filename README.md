# The Project Goal:
This project demonstrates the use of Apache Airflow with Docker, including a customized exchange rate (EUR/TWD) email alert based on data retrieved from Bank Sinopac (Taiwan) website.


# 🐳 Run Airflow in Docker
I was following this [doc](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
Here shows the steps to set up and run Apache Airflow in a Docker environment.

## 1. Check System Memory
Ensure your system has at least 4 GB of memory:

```
docker run --rm "debian:bookworm-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'
```
P.S. It will create a debian:bookworm-slim image, you can safely delete it if you don't plan to use it again.

## 2. Download docker-compose.yaml
Download the official Airflow Docker Compose file:
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.1/docker-compose.yaml'
```

## 3. Create Required Folders
```
mkdir -p ./dags ./logs ./plugins ./config
```

## 4. Set Up Environment File
```
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
It will create a .env file with your system UID.


## 5. Initialize the Database
```
docker compose up airflow-init
```

## 6. Clean Up (Optional)
To clean up volumes and orphan containers:
```
docker compose down --volumes --remove-orphans
```

## 7. Start All Services
Start all Airflow services:

```
docker compose up
```

# Additional Notes
To support custom **/data** paths and **user-defined functions**, additional volume mappings have been configured in the docker-compose.yaml file as follows:

```
volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
    - ./data:/data # mount data folder
    - ./:/opt/airflow/ # mount all files in the current directory
```