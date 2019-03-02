CREATE TABLE [dbo].[Population]
(
	[Id] INT NOT NULL PRIMARY KEY NONCLUSTERED, 
    [MedianIncome] MONEY NOT NULL, 
    [GDPPerCapita] MONEY NOT NULL, 
    [ContainsRepresentative] BIT NOT NULL, 
    [ElectionYear] DATE NOT NULL, 
    [TotalPopulation] INT NOT NULL, 
    [PrecinctId] INT NOT NULL, 
    CONSTRAINT [FK_Population_Precinct] FOREIGN KEY ([PrecinctId]) REFERENCES [Precinct]([Id]) 
)

GO

CREATE CLUSTERED INDEX [IX_Population_PrecinctId_ElectionYear] ON [dbo].[Population] ([PrecinctId], [ElectionYear])
