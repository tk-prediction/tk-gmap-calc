#!/bin/bash

crontab -l > crontab_bk.txt
crontab crontab_conf.txt