FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv socat
RUN python3 -m venv /home/ctfuser/venv

WORKDIR /home/ctfuser
COPY *.py /home/ctfuser/
ENV FLAG MOCSCTF{wr1t3_un1t_t3st5_f0r_y0ur_s4n1ty}
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 /home/ctfuser/venv/bin/python3 /home/ctfuser/chall.py"
