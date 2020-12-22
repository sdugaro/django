1. populate mongoDB database collections

> mongoimport --db retail --collection transactions --drop --type csv --headerline --file data/online_retail_data.csv 
> mongoimport --db retail --collection marketing --drop --jsonArray marketing_data.json

2. install flexmonster mongo connector and run the middleware server

> cd pivot-mongo
> npm install
> npm run build
> npm run start

3. launch the django server

> cd ..
> ./manage.py runserver


