FROM ubuntu:24.04 AS app

RUN apt update && apt upgrade -y && apt install -y xinetd
RUN groupadd -r user && useradd -r -g user user

COPY --chown=root:user ./coding-agent /home/user/coding-agent
COPY --chown=root:root ./ctf.conf /etc/xinetd.d/ctf
COPY --chown=root:user ./flag.txt /flag.txt

RUN chmod 555 /home/user/coding-agent
RUN chmod 444 /flag.txt
RUN chmod 444 /etc/xinetd.d/ctf

USER user

EXPOSE 31200

CMD ["xinetd", "-dontfork", "-f", "/etc/xinetd.d/ctf"]