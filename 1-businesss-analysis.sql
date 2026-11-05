USE RetailSalesDB;
GO

SELECT
    COUNT(*) AS TotalSalesInvoices,
    COUNT(DISTINCT CustomerID) AS IdentifiableCustomers,
    SUM(OrderValue) AS TotalSales,
    AVG(OrderValue) AS AverageOrderValue
FROM
(
    SELECT
        InvoiceNo,
        CustomerID,
        SUM(Quantity * UnitPrice) AS OrderValue
    FROM dbo.Online_Retail_Cleaned
    WHERE
        InvoiceNo NOT LIKE 'C%'
        AND Quantity > 0
        AND UnitPrice > 0
        AND InvoiceDate IS NOT NULL
    GROUP BY InvoiceNo, CustomerID
) AS SalesOrders;
GO