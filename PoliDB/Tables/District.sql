CREATE TABLE [dbo].[District]
(
	[Id] INT NOT NULL PRIMARY KEY NONCLUSTERED, 
    [State] VARCHAR(2) NOT NULL, 
    [Description] NVARCHAR(200) NOT NULL
)

GO

CREATE CLUSTERED INDEX [IX_District_State] ON [dbo].[District] ([State])
