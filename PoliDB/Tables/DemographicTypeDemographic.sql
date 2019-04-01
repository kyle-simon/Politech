CREATE TABLE [dbo].[DemographicTypeDemographic]
(
	[Id] INT NOT NULL PRIMARY KEY NONCLUSTERED, 
    [DemographicId] INT NOT NULL, 
    [DemographicTypeId] INT NOT NULL, 
    [Population] INT NOT NULL, 
    CONSTRAINT [FK_DemographicTypeDemographic_Demographic] FOREIGN KEY ([DemographicId]) REFERENCES [Demographic]([Id])
)		

GO

CREATE CLUSTERED INDEX [IX_DemographicTypeDemographic_DemographicId_DemographicTypeId] ON [dbo].[DemographicTypeDemographic] ([DemographicId], [DemographicTypeId])
