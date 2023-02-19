# Qrcode-Photo-Replacer

## Introduction

A dockerized tool for replacing the photo in qrcode, based on shadowsocks, flask and nginx. Using this tool with [iptables](!https://en.wikipedia.org/wiki/Iptables#:~:text=iptables%20is%20a%20user%2Dspace,to%20treat%20network%20traffic%20packets.) is highly recommended.

## Environment Requirement

1. Docker
2. [iptables](!https://en.wikipedia.org/wiki/Iptables#:~:text=iptables%20is%20a%20user%2Dspace,to%20treat%20network%20traffic%20packets.)

## Usage 

1. Setup the **password** in the environment `PASSWORD=password` in dockercompose.yml.
2. Place the SSL keys in `./nginx/ssl`, named "example.crt" and "example.key".
3. Place the photo file named "photo.jpg" in `./flask/`.
4. Run `docker-compos up -d` in shell.