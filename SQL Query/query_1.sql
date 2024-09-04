SELECT 
    i.InvoiceID,
    i.BillingDate,
    c.CustomerName AS CustomerName,
    rc.CustomerName AS ReferringCustomerName
FROM 
    Invoices i
LEFT JOIN
    Customers c ON i.CustomerID = c.CustomerID
LEFT JOIN 
    Customers rc ON c.ReferringCustomerID = rc.CustomerID
ORDER BY 
    i.BillingDate;
