insert into exchange_rates (
select ts, from_currency, to_currency, rate from (
select date_trunc('second', dd + (random() * 60) * '1 second':: interval) as ts, case when random()*2 < 1 then 'EUR' else 'USD' end as from_currency,
'GBP' as to_currency, (200 * random():: int )/100 as rate
FROM generate_series
        ( '2018-04-01'::timestamp
        , '2018-04-02'::timestamp
        , '1 minute'::interval) dd
     ) a
where ts not in (select ts from exchange_rates)
order by ts
)
;

insert into transactions (
SELECT dd + (random()*5) * '1 second'::interval as ts, (random() * 1000)::int as user_id,
case when random()*2 < 1 then 'EUR' else 'USD' end as currency,
(random() * 10000) :: int / 100 as amount
FROM generate_series
        ( '2018-04-01'::timestamp
        , '2018-04-02'::timestamp
        , '1 second'::interval) dd
)
;
