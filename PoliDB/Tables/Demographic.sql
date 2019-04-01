CREATE TABLE [dbo].[Demographic]
(
	[Id] INT NOT NULL PRIMARY KEY NONCLUSTERED, 
    --[MedianIncome] MONEY NOT NULL, 
    --[GDPPerCapita] MONEY NOT NULL, 
    [ContainsRepresentative] BIT NULL, 
    [Year] DATE NOT NULL, 
    [TotalPopulation] INT NULL, 
    [PrecinctId] INT NOT NULL, 
    CONSTRAINT [FK_Demographic_Precinct] FOREIGN KEY ([PrecinctId]) REFERENCES [Precinct]([Id]) 
)

GO

CREATE CLUSTERED INDEX [IX_Demographic_PrecinctId_ElectionYear] ON [dbo].[Demographic] ([PrecinctId], [Year])
