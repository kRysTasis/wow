FROM node:10.17.0

WORKDIR /usr/src/wow/web/

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
	net-tools \
	sudo \
	bzip2 \
	curl \
	gcc \
	git \
	vim
RUN apt-get clean

RUN npm install -g yarn \
	&& yarn global add @vue/cli \
