FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN useradd -U -m -s /bin/sh ctf

WORKDIR /home/ctf

COPY ./questions.py ./flag.txt ./

RUN chmod 550 questions.py \
    && chmod 440 flag.txt \
    && chown -R root:ctf /home/ctf

RUN printf '#!/bin/sh\ncd /home/ctf && exec python3 -u questions.py\n' > /home/ctf/run \
    && chmod 750 /home/ctf/run \
    && chown root:ctf /home/ctf/run

# ENSURE THE PORT YOU WANT TO USE IS NOT CURRENTLY USED BY ANOTHER CHALLENGE
EXPOSE 13337

CMD socat TCP-LISTEN:13337,reuseaddr,fork EXEC:"/home/ctf/run",su=ctf,stderr
