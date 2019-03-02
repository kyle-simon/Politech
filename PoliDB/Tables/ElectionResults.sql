CREATE TABLE [dbo].[ElectionResults]
(
	[Id] INT NOT NULL PRIMARY KEY NONCLUSTERED, 
    [DemocraticVote] INT NOT NULL, 
    [RepublicanVote] INT NOT NULL, 
    [PrecinctId] INT NOT NULL, 
    [ElectionYear] DATE NOT NULL, 
    CONSTRAINT [FK_ElectionResults_Precinct] FOREIGN KEY ([PrecinctId]) REFERENCES [Precinct]([Id])
)

GO

CREATE CLUSTERED INDEX [IX_ElectionResults_PrecinctId_ElectionYear] ON [dbo].[ElectionResults] ([PrecinctId], [ElectionYear])
