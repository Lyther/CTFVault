FROM ubuntu:24.04 AS app

RUN apt update && apt upgrade -y && apt install -y xinetd
RUN groupadd -r user && useradd -r -g user user

COPY --chown=root:user ./diary /home/user/diary
COPY --chown=root:root ./ctf.conf /etc/xinetd.d/ctf
COPY --chown=root:user ./flag.txt /home/user/flag.txt

RUN chmod 555 /home/user/diary
RUN chmod 444 /home/user/flag.txt
RUN chmod 444 /etc/xinetd.d/ctf

USER user

EXPOSE 30080

CMD ["xinetd", "-dontfork", "-f", "/etc/xinetd.d/ctf"]