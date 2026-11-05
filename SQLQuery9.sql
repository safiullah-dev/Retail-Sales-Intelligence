USE RetailSalesDB;
GO

SELECT
    SUM(DuplicateCount - 1) AS ActualDuplicateRows
FROM
(
    SELECT COUNT(*) AS DuplicateCount
    FROM dbo.Online_Retail_Cleaned
    GROUP BY
        InvoiceNo,
        StockCode,
        Description,
        Quantity,
        InvoiceDate,
        UnitPrice,
        CustomerID,
        Country
    HAVING COUNT(*) > 1
) AS DuplicateCheck;
GO