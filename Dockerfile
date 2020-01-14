FROM python:3.7-stretch
COPY . .
RUN python3 -m venv .venv
RUN ["/bin/bash", "-c", "source .venv/bin/activate"] && pip3 install -r requirements.txt
RUN python3 setup.py install
EXPOSE 5000
RUN mv run.py build/lib
CMD cd build/lib && python3 run.py