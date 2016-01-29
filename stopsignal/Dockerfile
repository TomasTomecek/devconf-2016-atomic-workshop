FROM fedora:23
ENV PYTHONUNBUFFERED=1
# STOPSIGNAL SIGUSR1
COPY ./signal_printer.py /
CMD ["/signal_printer.py"]
