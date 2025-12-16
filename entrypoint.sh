#!/bin/bash
set -e
python -m hrms --stamp
python -m hrms --revision "Initial database setup"
python -m hrms --upgrade
python -m hrms --init-db
python -m hrms --run-server