CREATE TABLE [dbo].[EconomicData]
(
	[Id] INT NOT NULL PRIMARY KEY NONCLUSTERED, 
    [GDPPerCapita] MONEY NULL, 
    [MedianIncome] NCHAR(10) NULL, 
    [PrecinctId] INT NOT NULL, 
    [Year] DATE NOT NULL, 
    CONSTRAINT [FK_EconomicData_Precinct] FOREIGN KEY ([PrecinctId]) REFERENCES [Precinct]([Id])
)
