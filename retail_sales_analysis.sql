SELECT COUNT(DISTINCT transaction_id) As number_of_sales,
       COUNT(DISTINCT customer_id) AS number_of_customers,

       date AS purchase_date,
       DAYNAME(date) AS day_name,
       MONTHNAME(date) AS month_name,
       DAYOFMONTH(date) AS day_of_month,
       
       CASE
           WHEN age BETWEEN 0 AND 12 THEN 'Child'
           WHEN age BETWEEN 13 AND 18 THEN 'Youth'
           WHEN age BETWEEN 19 AND 30 THEN 'Young Adult'
           WHEN age BETWEEN 31 AND 40 THEN 'Adult'
           ELSE 'Senior'
       END AS age_buckets,
      
       CASE
            WHEN total_amount BETWEEN 0 AND 100 THEN 'Low spend'
            WHEN total_amount >100 AND total_amount <= 200 THEN 'Med spend'
            WHEN total_amount > 200 THEN 'High spend'
        END AS spend_buckets,

        SUM(quantity) AS unit_sold,
        SUM(total_amount) AS total_revenue,

        product_category,
        gender,
FROM
  "SHOPING_TRENDS"."TRANSACTIONS"."SALES_RECORDS"
GROUP BY ALL;
