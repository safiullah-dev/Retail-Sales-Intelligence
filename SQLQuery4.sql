USE RetailSalesDB;
GO

-- Create the destination table if it does not exist
IF OBJECT_ID('dbo.Online_Retail_Cleaned', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Online_Retail_Cleaned
    (
        InvoiceNo NVARCHAR(50) NOT NULL,
        StockCode NVARCHAR(50) NOT NULL,
        Description NVARCHAR(255) NULL,
        Quantity INT NOT NULL,
        InvoiceDate DATETIME2 NULL,
        UnitPrice FLOAT NOT NULL,
        CustomerID INT NULL,
        Country NVARCHAR(100) NOT NULL
    );
END;
GO

-- Import the CSV only if the table is empty
IF NOT EXISTS (
    SELECT 1 FROM dbo.Online_Retail_Cleaned
)
BEGIN
    BULK INSERT dbo.Online_Retail_Cleaned
    FROM 'C:\Users\SAFI\Documents\Retail-sales-intelligence\data\processed\Online_Retail_Cleaned.csv'
    WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDQUOTE = '"',
        CODEPAGE = '65001',
        KEEPNULLS,
        TABLOCK
    );
END;
GO

-- Verify the imported data
SELECT
    COUNT(*) AS TotalRows,
    COUNT(DISTINCT InvoiceNo) AS UniqueInvoices,
    COUNT(DISTINCT StockCode) AS UniqueProducts,
    COUNT(DISTINCT Country) AS Countries
FROM dbo.Online_Retail_Cleaned;
GO

SELECT TOP 10 *
FROM dbo.Online_Retail_Cleaned;
GO