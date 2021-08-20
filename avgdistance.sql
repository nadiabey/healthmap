.open homes.db
.headers on
.mode csv
.output diststats.csv
select npa, avg(great_circle_km) as avg_km, avg(great_circle_mi) as avg_mi from distance group by npa;
