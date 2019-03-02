CREATE TABLE [dbo].[PrecinctDistrict]
(
	[Id] INT NOT NULL PRIMARY KEY NONCLUSTERED, 
    [DistrictId] INT NOT NULL, 
    [PrecinctId] INT NOT NULL, 
    [FromYear] DATE NOT NULL, 
    [ToYear] DATE NULL, 
    CONSTRAINT [FK_PrecinctDistrict_Precinct] FOREIGN KEY ([PrecinctId]) REFERENCES [Precinct]([Id]), 
    CONSTRAINT [FK_PrecinctDistrict_District] FOREIGN KEY ([DistrictId]) REFERENCES [District]([Id])
)

GO

CREATE CLUSTERED INDEX [IX_PrecinctDistrict_DistrictId_PrecinctId_FromYear] ON [dbo].[PrecinctDistrict] ([DistrictId], [PrecinctId], [FromYear])
