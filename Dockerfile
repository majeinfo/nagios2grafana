FROM python:3.7
LABEL maintainer="jd@maje.biz"
ARG target_dir=/app
ADD requirements.txt ${target_dir}/
RUN pip install -r ${target_dir}/requirements.txt
RUN cd ${target_dir} && git clone https://github.com/majeinfo/nagios2grafana.git
EXPOSE 5000
WORKDIR ${target_dir}/nagios2grafana
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "nagios2grafana:app(nagios_status_file=\"/app/status.dat\")"]
