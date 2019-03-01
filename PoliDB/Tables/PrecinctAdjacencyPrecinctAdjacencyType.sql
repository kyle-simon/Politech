CREATE TABLE [dbo].[PrecinctAdjacencyPrecinctAdjacencyType]
(
	[Id] INT NOT NULL PRIMARY KEY, 
    [PrecinctAdjacencyId] INT NOT NULL, 
    [PrecinctAdjacencyTypeId] INT NOT NULL, 
    CONSTRAINT [FK_PrecinctAdjacencyPrecinctAdjacencyType_PrecinctAdjacency] FOREIGN KEY ([PrecinctAdjacencyId]) REFERENCES [PrecinctAdjacency]([Id]), 
    CONSTRAINT [FK_PrecinctAdjacencyPrecinctAdjacencyType_PrecinctAdjacencyType] FOREIGN KEY ([PrecinctAdjacencyTypeId]) REFERENCES [PrecinctAdjacencyType]([Id])
)
