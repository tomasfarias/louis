# db

This is the database part of the challenge. All queries ran are available under `sql/`.

## Setting up the database

The database provided runs as a Docker container deployed with `docker-compose`. The following queries are considered part of the setup and where obtained from the challenge instructions:
* ![01_create_schema.sql](sql/01_create_schema.sql): This query setups the `exchange_rates` and `transactions` tables, with data provided by the task.
* ![04_simulate_volumes_of_data.sql](sql/04_simulate_volumes_of_data.sql): After the first two analysis, this query inserts a decent volume of data into the `exchange_rates` and `transactions` tables to simulate more real-world conditions

## Usage

The database may be deployed with `docker-compose.yml`:

``` sh
docker-compose up -d database
```

Port 5432 is used for the PostgreSQL database. If it's already in use (by another PostgreSQL database maybe?) then a different port number must be chosen and edited into `docker-compose.yml`.

After the container starts, the database will be available in `localhost`, you can connect with the test credentials by running:

``` sh
psql -h localhost -p 5432 -U test -d test
```

Test credentials are available in ![`database.env`](../database.env).

### First task

The first task involved breaking down user expenditure in GBP using the latest exchange rate available for each currency pair. The results have been inserted into the `total_spent_gbp_by_user_latest_rate` table and may be queried as follows:

``` sql
SELECT * FROM total_spent_gbp_by_user_latest_rate;
```

The query used to build this table is available in ![02_spend_breakdown_latest_date.sql](sql/02_spend_breakdown_latest_date.sql).

### Second task

The second task was similar to the first one, but required obtaining the exchange rate with the largest closest timestamp to the transaction timestamp. This was achieved by means of a subquery, and the results are available at `total_spent_gbp_by_user_closest_rate`:

``` sql
SELECT * FROM total_spent_gbp_by_user_closest_rate;
```

The query used to build this table is available in ![03_spend_breakdown_closest_date.sql](sql/02_spend_breakdown_closest_date.sql).

Although you may run the queries in the database provided, keep in mind that by this point the volume of data has been increased substantially for the third and final task. So the results will not be comparable to the results available in `total_spent_gbp_by_user_closest_rate`.

### Third task

The third and final task was the same as the second one, but involved running the query against much larger tables. I didn't even tried running the query produced as the output of the Second task as I already expected performance to be pretty bad. After some re-writing, I arrived at the solution available in ![05_spend_breakdown_closest_date_fast.sql](sql/05_spend_breakdown_closest_date_fast.sql). As with the previous two tasks, results may be selected with:

``` sql
SELECT * FROM total_spent_gbp_by_user_closest_rate_fast;
```

To further improve query performance, I created a few indices for `exchange_rates` and `transactions`, and ran `VACUUM ANALYZE` on both tables to ensure PostgreSQL had up-to-date statistics.

A query plan is also available ![here](task_three_plan.json).

## Wiping and recreating the database

If you wish to completely recreate everything in the database to, for example, evaluate the queries again, tear down the `docker-compose` deployment first (if it's running):

``` sh
docker-compose down
```

Then wipe the database volume with the following

``` sh
rm -rf db/data/
```

**WARNING**: Triple check what you are removing otherwise this step could have catastrophic consequences. The database volume is by default located in `db/data/` but review the `docker-compose.yml` file to ensure this is still true, and that there's nothing else of value contained in the volume.

Starting up the database again should re-run all queries:

``` sh
docker-compose up -d databse
```
