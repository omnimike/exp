FROM archlinux/base:latest

WORKDIR /root

RUN pacman -Sy --noconfirm openssh

COPY ssh/* /etc/ssh/
RUN ssh-keygen -t rsa -N "" -f /etc/ssh/ssh_host_rsa_key

EXPOSE 2222

CMD ["/usr/sbin/sshd", "-D"]

