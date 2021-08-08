CREATE TABLE total_spent_gbp_by_user_latest_rate (
  user_id INT,
  total_spent_gbp NUMERIC
);

INSERT INTO total_spent_gbp_by_user_latest_rate
WITH numbered_exchange_rates AS (
  SELECT
    from_currency,
    to_currency,
    rate,
    ROW_NUMBER() OVER (PARTITION BY from_currency, to_currency ORDER BY ts DESC) AS rn
  FROM
    exchange_rates
),

gbp_transactions AS (
  SELECT
    t.user_id,
    t.amount,
    (
      CASE
        WHEN t.currency != 'GBP' THEN e.rate
        ELSE 1
      END
    ) AS rate
  FROM
    transactions AS t LEFT JOIN numbered_exchange_rates AS e
  ON
    e.from_currency = t.currency
    AND e.to_currency = 'GBP'
    AND e.rn = 1
)

SELECT
  user_id,
  SUM(rate * amount) AS total_gbp_amount
FROM
  gbp_transactions
GROUP BY
  user_id
ORDER BY
  user_id
;
