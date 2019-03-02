CREATE TABLE [dbo].[DemographicTypePopulation]
(
	[Id] INT NOT NULL PRIMARY KEY NONCLUSTERED, 
    [PopulationId] INT NOT NULL, 
    [DemographicTypeId] INT NOT NULL, 
    [Population] INT NOT NULL
)

GO

CREATE CLUSTERED INDEX [IX_DemographicTypePopulation_PopulationId_DemographicTypeId] ON [dbo].[DemographicTypePopulation] ([PopulationId], [DemographicTypeId])
