@echo off

coverage run -m pytest tests/ -v
coverage report -m
