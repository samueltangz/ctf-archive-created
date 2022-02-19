FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv socat
RUN python3 -m venv /home/ctfuser/venv

WORKDIR /home/ctfuser
COPY *.py /home/ctfuser/
ENV FLAG MOCSCTF{c4n_y0u_pr3d1c7_th3_4ctu4l_w0rd13_s0lu71on5_n0w}
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 /home/ctfuser/venv/bin/python3 /home/ctfuser/chall.py"
