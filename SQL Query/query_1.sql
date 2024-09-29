SELECT 
    i.Id,
    i.BillingDate,
    c.Name AS CustomerName,
    rc.Name AS ReferringCustomerName
FROM 
    Invoices i
LEFT JOIN
    Customers c ON i.CustomerID = c.Id
LEFT JOIN 
    Customers rc ON c.ReferredBy = rc.Id
ORDER BY 
    i.BillingDate;
