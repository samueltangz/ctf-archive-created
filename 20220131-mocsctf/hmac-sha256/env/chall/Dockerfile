FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv socat
RUN python3 -m venv /home/ctfuser/venv

WORKDIR /home/ctfuser
COPY *.py /home/ctfuser/
ENV FLAG MOCSCTF{wh4t_i5_th3_u53_0f_5uch_c0111si0ns_w1th_d1ff3ren7_k3y5}
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 /home/ctfuser/venv/bin/python3 /home/ctfuser/chall.py"
