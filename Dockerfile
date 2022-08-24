FROM python:3.9-slim
LABEL maintainer="jd@maje.biz"
ARG target_dir=/app
ARG config_dir=/config

ADD requirements.txt ${target_dir}/
RUN apt-get -y update && apt-get -y install git && apt-get clean
RUN pip install -r ${target_dir}/requirements.txt
RUN cd ${target_dir} && git clone https://github.com/majeinfo/nagios2grafana.git && rm -rf nagios2grafana/.git

EXPOSE 5000
WORKDIR ${target_dir}/nagios2grafana
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "nagios2grafana:app(nagios_status_file=\"/config/status.dat\")"]
