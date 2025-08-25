-- Check the number of customers and their average account balances by customer type:
SELECT	CT.customer_type,
		COUNT(C.customer_id) AS customer_count,
		ROUND(AVG(A.balance),2) AS average_balance
FROM CustomerTypes CT JOIN Customers C ON CT.type_id = C.type_id
JOIN Accounts A ON C.customer_id = A.customer_id
WHERE A.date_closed IS NULL
GROUP BY CT.customer_type;

-- Check the contact information of customers whose accounts have been closed due to suspicious activity:
SELECT	DISTINCT C.customer_id,
		P.last_name, P.first_name,
		P.phone_number, P.email,
		A.street, A.postal_code, A.city, A.country
FROM Addresses A JOIN Persons P ON A.address_id = P.address_id
JOIN Customers C ON P.person_id = C.customer_id
JOIN Accounts Ac ON C.customer_id = Ac.customer_id
JOIN AccountStatus AcS ON Ac.status_id = AcS.status_id
WHERE AcS.reason = "Suspicious Activity"
ORDER BY C.customer_id;

-- Count the proportion of defaults on loans each branch has experienced:
SELECT 	B2.branch_id,
		B2.branch_name,
		COUNT(L2.loan_id) AS total_loans,
		total_defaults,
		ROUND(CAST(total_defaults AS FLOAT) / CAST(COUNT(L2.loan_id) AS FLOAT),4) AS proportion
FROM LoanStatus LS2 JOIN Loans L2 ON LS2.status_id = L2.status_id
JOIN Customers C2 ON L2.customer_id = C2.customer_id
JOIN Accounts A2 ON C2.customer_id = A2.customer_id
JOIN Branches B2 ON A2.branch_id = B2.branch_id
JOIN (
	SELECT	B1.branch_id AS B1_id,
			COUNT(L1.loan_id) AS total_defaults
	FROM LoanStatus LS1 JOIN Loans L1 ON LS1.status_id = L1.status_id
	JOIN Customers C1 ON L1.customer_id = C1.customer_id
	JOIN Accounts A1 ON C1.customer_id = A1.customer_id
	JOIN Branches B1 ON A1.branch_id = B1.branch_id
	WHERE LS1.loan_status = "Default"
	GROUP BY B1.branch_id, B1.branch_name
) ON B1_id = B2.branch_id
GROUP BY B2.branch_id, B2.branch_name
ORDER BY B2.branch_id;


