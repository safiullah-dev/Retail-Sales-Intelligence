USE RetailSalesDB;
GO

-- 1. Verify total records
SELECT COUNT(*) AS TotalRows
FROM dbo.Online_Retail_Cleaned;
GO

-- 2. Verify duplicate records
SELECT COUNT(*) AS DuplicateRows
FROM
(
    SELECT
        InvoiceNo,
        StockCode,
        InvoiceDate,
        Quantity,
        UnitPrice,
        COUNT(*) AS DuplicateCount
    FROM dbo.Online_Retail_Cleaned
    GROUP BY
        InvoiceNo,
        StockCode,
        InvoiceDate,
        Quantity,
        UnitPrice
    HAVING COUNT(*) > 1
) AS Duplicates;
GO

-- 3. Verify missing values
SELECT
    SUM(CASE WHEN Description IS NULL THEN 1 ELSE 0 END)
        AS MissingDescriptions,
    SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END)
        AS MissingCustomerIDs
FROM dbo.Online_Retail_Cleaned;
GO

-- 4. Verify invalid quantities and prices
SELECT
    SUM(CASE WHEN Quantity < 0 THEN 1 ELSE 0 END)
        AS NegativeQuantities,
    SUM(CASE WHEN UnitPrice < 0 THEN 1 ELSE 0 END)
        AS NegativePrices,
    SUM(CASE WHEN UnitPrice = 0 THEN 1 ELSE 0 END)
        AS ZeroPrices
FROM dbo.Online_Retail_Cleaned;
GO