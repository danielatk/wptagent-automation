#!/bin/sh

# Habilitação do TCP BBR
BRR=n
read -p 'Habilitar TCP BBR? [y/n]' BBR
if [ BBR = y]; then
    sudo modprobe tcp_bbr
    echo 'net.ipv4.tcp_congestion_control = bbr' | sudo tee -a /etc/sysctl.conf
    echo 'net.core.default_qdisc = fq' | sudo tee -a /etc/sysctl.conf
    sudo sysctl -p

    if [ $(sysctl net.ipv4.tcp_congestion_control | sed 's/^.*= //') = bbr ]; then
        echo 'TCP BBR habilitado com sucesso.'
    else
        echo 'Não foi possível habilitar o TCP BBR, por favor verifique.'
    fi
fi