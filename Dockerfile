FROM python:3.7
WORKDIR /
RUN https://github.com/majeinfo/nagios2grafana.git
RUN pip install -r requirements.txt
COPY docker-entrypoint.sh /
ENV LISTEN_PORT 5000
ENV NAGIOS_STATUS_FILE /var/lib/nagios/status.dat
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "nagios2grafana:app(nagios_status_file=\"/nagios/status.dat\")"]
