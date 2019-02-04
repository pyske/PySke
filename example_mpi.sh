#!/bin/bash

mpiexec -hostfile myhostfile.txt -n 4 python3 pyske_para.py
