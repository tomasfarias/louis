CREATE INDEX from_currency_index ON exchange_rates (from_currency);
CREATE INDEX to_currency_index ON exchange_rates (to_currency);
CREATE INDEX exchange_rate_ts_index ON exchange_rates (ts);
CREATE INDEX currency_index ON transactions (currency);
CREATE INDEX transaction_ts_index ON transactions (ts);
CREATE INDEX user_id_index ON transactions (user_id);

VACUUM ANALYZE transactions;
VACUUM ANALYZE exchange_rates;

CREATE TABLE total_spent_gbp_by_user_closest_rate_fast (
  user_id INT,
  total_spent_gbp NUMERIC
);

INSERT INTO total_spent_gbp_by_user_closest_rate_fast
WITH closest_dates AS (
  SELECT
    t.user_id,
    t.amount * (
      SELECT
      (
        CASE WHEN t.currency = 'GBP' THEN 1
        ELSE e.rate
        END
      ) AS rate
      FROM
        exchange_rates AS e
      WHERE
        e.ts <= t.ts
        AND e.from_currency = t.currency
        AND e.to_currency = 'GBP'
      ORDER BY
        e.ts
      DESC
      LIMIT 1
  ) AS gbp_amount
  FROM
    transactions AS t
)
SELECT
  user_id,
  SUM(gbp_amount) AS total_gbp_amount
FROM
  closest_dates
GROUP BY
  user_id
ORDER BY
  user_id
;
