# CheRM
Chemical Compounds Recommender Matrix


## 1. Dump mySQL chebi database
## 2. Create chebi_rec_sys database using chebi_rec_sys_tables.sql
Run ```ALTER TABLE articles MODIFY title TEXT CHARACTER SET utf8;``` for changing the column title from articles to utf8

## 3. ```docker build -t chebisys .```
## Change the credentials for the databases in the main.py file 
## 4. ```docker run --net=host -v /path/for/data:/mlData -v /home/uname/chebi_rec_sys/config:/config -v /home/uname/chebi_rec_sys/src:/src_ chebisys```

## 5. In /create_CheRM/create_user_item_rating.py change the credentials for the database cheby_rec_sys and run this python file for creating CheRM


## The files necessary for this software are available for download at: 