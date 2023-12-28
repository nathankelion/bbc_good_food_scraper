USE BBC_Good_Food;

-- Drop tables if they exist
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS nutrition;
DROP TABLE IF EXISTS recipe_info;

-- Create the recipe_info table
CREATE TABLE recipe_info (
    recipe_id		INT PRIMARY KEY NOT NULL,
    RecipeName		VARCHAR(100),
    RecipeLink		VARCHAR(200),
    CookingTime		VARCHAR(10),
    HealthStatus	VARCHAR(25),
	Diet			VARCHAR(25),
	Difficulty		VARCHAR(25)
);

-- Create the nutrition table
CREATE TABLE nutrition (
	recipe_id		INT NOT NULL,
	kcal			INT,
	[Fat(g)]		FLOAT,
	[Saturates(g)]	FLOAT,
	[Carbs(g)]		FLOAT,
	[Sugars(g)]		FLOAT,
	[Fibre(g)]		FLOAT,
	[Protein(g)]	FLOAT,
	[Salt(g)]		FLOAT,
	FOREIGN KEY (recipe_id) REFERENCES recipe_info(recipe_id)
);

CREATE TABLE ingredients (
	recipe_id		INT NOT NULL,
	Ingredient		VARCHAR(200)
	FOREIGN KEY (recipe_id) REFERENCES recipe_info(recipe_id)
);