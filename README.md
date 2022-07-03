# real_estate_scrapper

## Description

Web scrapper for REMAX website to look for triplexes and send emails when posting meets hard coded criterias

Current criteria is Price <= 850,000$

The Scrapper needs two csv files to be setup as follow :

1. sender.csv

This file needs to have the email adress and password of the sender formatted as follow :
email@adress.com,password

2.receiver.csv

This a list of email adress that are going to receive an email. Formatting is as follow :
email1@adress.com,email2@adress.com,....