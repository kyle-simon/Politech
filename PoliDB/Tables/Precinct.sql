CREATE TABLE [dbo].[Precinct]
(
	[Id] INT NOT NULL PRIMARY KEY, 
    [PrecinctShape] [sys].[geography] NOT NULL, 
    [State] VARCHAR(2) NULL
)
