FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv socat
RUN python3 -m venv /home/ctfuser/venv

RUN /home/ctfuser/venv/bin/pip uninstall crypto
RUN /home/ctfuser/venv/bin/pip uninstall pycryptodome
RUN /home/ctfuser/venv/bin/pip install pycryptodome

WORKDIR /home/ctfuser
COPY *.py /home/ctfuser/
ENV FLAG MOCSCTF{i_sh0uld_u5e_AND_0xff_in5t3ad_0f_M0D_0xff}
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 /home/ctfuser/venv/bin/python3 /home/ctfuser/chall.py"
