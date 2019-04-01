CREATE TABLE [dbo].[PrecinctAdjacency]
(
	[Id] INT NOT NULL PRIMARY KEY NONCLUSTERED, 
    [PrecinctId1] INT NOT NULL, 
    [PrecinctId2] INT NOT NULL, 
    CONSTRAINT [FK_PrecinctAdjacency_Precinct1] FOREIGN KEY ([PrecinctId1]) REFERENCES [Precinct]([Id]), 
    CONSTRAINT [FK_PrecinctAdjacency_Precinct2] FOREIGN KEY ([PrecinctId2]) REFERENCES [Precinct]([Id])
)

GO

CREATE CLUSTERED INDEX [IX_PrecinctAdjacency_PrecinctId1_PrecinctId2] ON [dbo].[PrecinctAdjacency] ([PrecinctId1], [PrecinctId2])
