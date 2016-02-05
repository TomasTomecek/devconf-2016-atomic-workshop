FROM fedora
ENV PYTHONUNBUFFERED=1
RUN dnf install -y iproute iputils
CMD ["python3", "-m", "http.server", "8000"]

