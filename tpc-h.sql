CREATE DATABASE [TPCH] ON  PRIMARY
GO

CREATE TABLE [dbo].[customer](
    [C_CustKey] [int] NULL,
    [C_Name] [varchar](64) NULL,
    [C_Address] [varchar](64) NULL,
    [C_NationKey] [int] NULL,
    [C_Phone] [varchar](64) NULL,
    [C_AcctBal] [decimal](13, 2) NULL,
    [C_MktSegment] [varchar](64) NULL,
    [C_Comment] [varchar](120) NULL,
    [skip] [varchar](64) NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[lineitem](
    [L_OrderKey] [int] NULL,
    [L_PartKey] [int] NULL,
    [L_SuppKey] [int] NULL,
    [L_LineNumber] [int] NULL,
    [L_Quantity] [int] NULL,
    [L_ExtendedPrice] [decimal](13, 2) NULL,
    [L_Discount] [decimal](13, 2) NULL,
    [L_Tax] [decimal](13, 2) NULL,
    [L_ReturnFlag] [varchar](64) NULL,
    [L_LineStatus] [varchar](64) NULL,
    [L_ShipDate] [datetime] NULL,
    [L_CommitDate] [datetime] NULL,
    [L_ReceiptDate] [datetime] NULL,
    [L_ShipInstruct] [varchar](64) NULL,
    [L_ShipMode] [varchar](64) NULL,
    [L_Comment] [varchar](64) NULL,
    [skip] [varchar](64) NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[nation](
    [N_NationKey] [int] NULL,
    [N_Name] [varchar](64) NULL,
    [N_RegionKey] [int] NULL,
    [N_Comment] [varchar](160) NULL,
    [skip] [varchar](64) NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[orders](
    [O_OrderKey] [int] NULL,
    [O_CustKey] [int] NULL,
    [O_OrderStatus] [varchar](64) NULL,
    [O_TotalPrice] [decimal](13, 2) NULL,
    [O_OrderDate] [datetime] NULL,
    [O_OrderPriority] [varchar](15) NULL,
    [O_Clerk] [varchar](64) NULL,
    [O_ShipPriority] [int] NULL,
    [O_Comment] [varchar](80) NULL,
    [skip] [varchar](64) NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[part](
    [P_PartKey] [int] NULL,
    [P_Name] [varchar](64) NULL,
    [P_Mfgr] [varchar](64) NULL,
    [P_Brand] [varchar](64) NULL,
    [P_Type] [varchar](64) NULL,
    [P_Size] [int] NULL,
    [P_Container] [varchar](64) NULL,
    [P_RetailPrice] [decimal](13, 2) NULL,
    [P_Comment] [varchar](64) NULL,
    [skip] [varchar](64) NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[partsupp](
    [PS_PartKey] [int] NULL,
    [PS_SuppKey] [int] NULL,
    [PS_AvailQty] [int] NULL,
    [PS_SupplyCost] [decimal](13, 2) NULL,
    [PS_Comment] [varchar](200) NULL,
    [skip] [varchar](64) NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[region](
    [R_RegionKey] [int] NULL,
    [R_Name] [varchar](64) NULL,
    [R_Comment] [varchar](160) NULL,
    [skip] [varchar](64) NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[supplier](
    [S_SuppKey] [int] NULL,
    [S_Name] [varchar](64) NULL,
    [S_Address] [varchar](64) NULL,
    [S_NationKey] [int] NULL,
    [S_Phone] [varchar](18) NULL,
    [S_AcctBal] [decimal](13, 2) NULL,
    [S_Comment] [varchar](105) NULL,
    [skip] [varchar](64) NULL
) ON [PRIMARY]
GO

BULK INSERT part FROM '/home/nghia/Documents/tpch_2.18.0_rc2/dbgen/part.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|')
BULK INSERT customer FROM '/home/nghia/Documents/tpch_2.18.0_rc2/dbgen/customer.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|')
BULK INSERT orders FROM '/home/nghia/Documents/tpch_2.18.0_rc2/dbgen/orders.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|')
BULK INSERT partsupp FROM '/home/nghia/Documents/tpch_2.18.0_rc2/dbgen/partsupp.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|')
BULK INSERT supplier FROM '/home/nghia/Documents/tpch_2.18.0_rc2/dbgen/supplier.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|')
BULK INSERT lineitem FROM '/home/nghia/Documents/tpch_2.18.0_rc2/dbgen/lineitem.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|')
BULK INSERT nation FROM '/home/nghia/Documents/tpch_2.18.0_rc2/dbgen/nation.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|')
BULK INSERT region FROM '/home/nghia/Documents/tpch_2.18.0_rc2/dbgen/region.tbl' WITH (TABLOCK, DATAFILETYPE='char', CODEPAGE='raw', FIELDTERMINATOR = '|')
