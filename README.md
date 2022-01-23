# CheRM
Chemical Compounds Recommender Matrix

CheRM is a dataset of Chemical Compounds with the format of <user,item,rating> where the users are authors from articles, the items are Chemical Compounds from ChEBI, and the ratings are the number of articles each author wrote about an item.

The goal of this dataset is to be use by collaborative-filtering recommender systems engines for recommending Chemical Compounds of interest for the researchers from the Chemistry field.
Follow the steps bellow for creating your own dataset, or download it from: https://drive.google.com/drive/folders/1AbYgGw7V7KgSLudwxBAbH4yZrwHlBuFG?usp=sharing

## Requirements:
* Docker


## 1. 
Dump mySQL chebi database
## 2. 
Create chebi_rec_sys database using chebi_rec_sys_tables.sql

Run ```ALTER TABLE articles MODIFY title TEXT CHARACTER SET utf8;``` for changing the column title from articles to utf8

## 3. For docker:
```
docker build -t cherm .

docker run -t -d --name cherm_container --net=host -v /path/to/data/folder:/mlData -v /path/to/CheRM:/CheRM cherm

docker exec -it cherm_container bash

```
# 4. Create the database of articles

```
cd CheRM/chebi_rec_sys
Change the credentials for the databases in the main.py file 
python main.py

```

## 4. create the recommendation dataset <author,chemical,rating>
```
cd create_CheRM
python create_user_item_rating.py
```
note: change the credentials for the database cheby_rec_sys

## 6. create the recommendation sequential dataset 
```
cd create_CheRM
python create_user_item_rating_year.py
```



