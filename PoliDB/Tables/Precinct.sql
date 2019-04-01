CREATE TABLE [dbo].[Precinct]
(
	[Id] INT NOT NULL PRIMARY KEY NONCLUSTERED, 
    [PrecinctShape] [sys].[geography] NOT NULL, 
    [State] VARCHAR(2) NOT NULL, 
    [Description] NVARCHAR(200) NOT NULL
)

GO

CREATE CLUSTERED INDEX [IX_Precinct_State_Description] ON [dbo].[Precinct] ([State], [Description])
