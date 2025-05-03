-- No so good SQL Code for Review
SELECT * 
FROM customers 
WHERE status = 'active'
AND register_date > '2022-01-01'
OR status = 'inactive'
ORDER BY customer_name;
