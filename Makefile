#!/bin/bash
include .env
export $(shell sed 's/=.*//' .env)

.PHONY: install
install:
	@sh install.sh
	@pip3 install -r requirements.txt
	@python3 main.py --migrate -y
	@python3 main.py --validate-sources
	@python3 main.py

.PHONY: run
run:
	@python3 main.py

.PHONY: help
help:
	@python3 main.py --help
