CREATE TABLE [dbo].[PrecinctAdjacency]
(
	[Id] INT NOT NULL PRIMARY KEY, 
    [PrecinctId1] INT NOT NULL, 
    [PrecinctId2] INT NOT NULL, 
    CONSTRAINT [FK_PrecinctAdjacency_Precinct1] FOREIGN KEY ([PrecinctId1]) REFERENCES [Precinct]([Id]), 
    CONSTRAINT [FK_PrecinctAdjacency_Precinct2] FOREIGN KEY ([PrecinctId2]) REFERENCES [Precinct]([Id])
)
