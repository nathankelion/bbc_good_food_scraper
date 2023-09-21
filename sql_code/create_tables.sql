USE BBC_Good_Food
GO

-- Create the recipe_info table
CREATE TABLE recipe_info (
    recipe_id		INT PRIMARY KEY NOT NULL,
    [Recipe Name]	VARCHAR(75),
    [Recipe Links]	VARCHAR(100) NOT NULL,
    [Cooking Time]	TIME,
    [Heath Status]	VARCHAR(15),
	[Diet]			VARCHAR(15),
	[Difficulty]	VARCHAR(15)
)
GO

-- Create the nutrition table
CREATE TABLE nutrition (
	recipe_id		INT NOT NULL,
	[kcal]			INT,
	[Fat (g)]		FLOAT,
	[Saturates (g)] FLOAT,
	[Carbs (g)]		FLOAT,
	[Sugars (g)]	FLOAT,
	[Fibre (g)]		FLOAT,
	[Protein (g)]	FLOAT,
	[Salt (g)]		FLOAT,
	FOREIGN KEY (recipe_id) REFERENCES recipe_info(recipe_id)
);