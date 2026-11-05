USE RetailSalesDB;
GO

-- 1. Overall data verification
SELECT
    COUNT(*) AS TotalRows,
    COUNT(DISTINCT InvoiceNo) AS UniqueInvoices,
    COUNT(DISTINCT StockCode) AS UniqueProducts,
    COUNT(DISTINCT Country) AS UniqueCountries
FROM dbo.Online_Retail_Cleaned;
GO

-- 2. Sales performance KPIs
SELECT
    COUNT(DISTINCT InvoiceNo) AS TotalSalesInvoices,
    COUNT(DISTINCT CustomerID) AS IdentifiableCustomers,
    SUM(Quantity * UnitPrice) AS TotalSales,
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

-- 3. Monthly sales trend
SELECT
    YEAR(InvoiceDate) AS SalesYear,
    MONTH(InvoiceDate) AS SalesMonth,
    SUM(Quantity * UnitPrice) AS MonthlySales,
    COUNT(DISTINCT InvoiceNo) AS MonthlyOrders
FROM dbo.Online_Retail_Cleaned
WHERE
    InvoiceNo NOT LIKE 'C%'
    AND Quantity > 0
    AND UnitPrice > 0
    AND InvoiceDate IS NOT NULL
GROUP BY YEAR(InvoiceDate), MONTH(InvoiceDate)
ORDER BY SalesYear, SalesMonth;
GO

-- 4. Top 10 products by sales
SELECT TOP 10
    StockCode,
    MAX(Description) AS ProductName,
    SUM(Quantity * UnitPrice) AS TotalProductSales,
    SUM(Quantity) AS UnitsSold
FROM dbo.Online_Retail_Cleaned
WHERE
    InvoiceNo NOT LIKE 'C%'
    AND Quantity > 0
    AND UnitPrice > 0
GROUP BY StockCode
ORDER BY TotalProductSales DESC;
GO

-- 5. Top 10 countries by sales
SELECT TOP 10
    Country,
    SUM(Quantity * UnitPrice) AS TotalSales,
    COUNT(DISTINCT InvoiceNo) AS TotalOrders
FROM dbo.Online_Retail_Cleaned
WHERE
    InvoiceNo NOT LIKE 'C%'
    AND Quantity > 0
    AND UnitPrice > 0
GROUP BY Country
ORDER BY TotalSales DESC;
GO

-- 6. Top 10 customers by sales
SELECT TOP 10
    CustomerID,
    SUM(Quantity * UnitPrice) AS TotalCustomerSales,
    COUNT(DISTINCT InvoiceNo) AS TotalOrders
FROM dbo.Online_Retail_Cleaned
WHERE
    CustomerID IS NOT NULL
    AND InvoiceNo NOT LIKE 'C%'
    AND Quantity > 0
    AND UnitPrice > 0
GROUP BY CustomerID
ORDER BY TotalCustomerSales DESC;
GO

-- 7. Repeat customer analysis
WITH CustomerOrders AS
(
    SELECT
        CustomerID,
        COUNT(DISTINCT InvoiceNo) AS OrderCount
    FROM dbo.Online_Retail_Cleaned
    WHERE
        CustomerID IS NOT NULL
        AND InvoiceNo NOT LIKE 'C%'
        AND Quantity > 0
        AND UnitPrice > 0
    GROUP BY CustomerID
)
SELECT
    COUNT(*) AS TotalIdentifiableCustomers,
    SUM(CASE WHEN OrderCount > 1 THEN 1 ELSE 0 END)
        AS RepeatCustomers,
    CAST(
        100.0 * SUM(CASE WHEN OrderCount > 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0)
        AS DECIMAL(10,2)
    ) AS RepeatCustomerPercentage
FROM CustomerOrders;
GO

-- 8. Returns and cancelled transactions
SELECT
    COUNT(*) AS CancelledOrReturnRecords,
    COUNT(DISTINCT InvoiceNo) AS CancelledInvoiceNumbers,
    SUM(ABS(Quantity * UnitPrice)) AS ReturnValue
FROM dbo.Online_Retail_Cleaned
WHERE InvoiceNo LIKE 'C%' OR Quantity < 0;
GO