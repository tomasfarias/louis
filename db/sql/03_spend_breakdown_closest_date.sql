CREATE TABLE total_spent_gbp_by_user_closest_rate (
  user_id INT,
  total_spent_gbp NUMERIC
);

INSERT INTO total_spent_gbp_by_user_closest_rate
WITH gbp_transactions AS (
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
    transactions AS t LEFT JOIN exchange_rates AS e
    ON e.from_currency = t.currency
    AND e.to_currency = 'GBP'
    AND e.ts = (
      SELECT r.ts
      FROM exchange_rates AS r
      WHERE
        r.ts <= t.ts
        AND r.to_currency = 'GBP'
        AND r.from_currency = t.currency
      ORDER BY r.ts DESC
      LIMIT 1
    )
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
