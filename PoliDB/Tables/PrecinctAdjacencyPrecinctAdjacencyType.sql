CREATE TABLE [dbo].[PrecinctAdjacencyPrecinctAdjacencyType]
(
	[Id] INT NOT NULL PRIMARY KEY NONCLUSTERED, 
    [PrecinctAdjacencyId] INT NOT NULL, 
    [PrecinctAdjacencyTypeId] INT NOT NULL, 
    CONSTRAINT [FK_PrecinctAdjacencyPrecinctAdjacencyType_PrecinctAdjacency] FOREIGN KEY ([PrecinctAdjacencyId]) REFERENCES [PrecinctAdjacency]([Id]), 
    CONSTRAINT [FK_PrecinctAdjacencyPrecinctAdjacencyType_PrecinctAdjacencyType] FOREIGN KEY ([PrecinctAdjacencyTypeId]) REFERENCES [PrecinctAdjacencyType]([Id])
)

GO

CREATE INDEX [IX_PrecinctAdjacencyPrecinctAdjacencyType_PrecinctAdjacencyId] ON [dbo].[PrecinctAdjacencyPrecinctAdjacencyType] ([PrecinctAdjacencyId])
