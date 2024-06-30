

check_pythonpath() {
    if [ -z "${PYTHONPATH}" ]; then
        echo "PYTHONPATH is not set!"
        exit 1
    else
        echo "PYTHONPATH is set to: ${PYTHONPATH}"
    fi
}
airflow db upgrade

airflow users create -r Admin -u admin -p admin -e admin@example.com -f admin -l airflow
# "$_AIRFLOW_WWW_USER_USERNAME" -p "$_AIRFLOW_WWW_USER_PASSWORD"

airflow webserver