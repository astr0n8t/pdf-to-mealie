# FROM https://github.com/mealie-recipes/mealie/discussions/4490#discussioncomment-11323364

import json
import requests
from pathlib import Path
import time
import os
from dotenv import load_dotenv

class MealieImporter:
    def __init__(self):
        load_dotenv()
        
        self.host = os.getenv('MEALIE_HOST', 'http://127.0.0.1:8000')
        self.api_key = os.getenv('MEALIE_API_KEY')
        
        if not self.api_key:
            raise ValueError("MEALIE_API_KEY not found in .env file")
            
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def import_recipe(self, recipe_json):
        """Import a recipe to Mealie using the html-or-json endpoint"""
        url = f"{self.host}/api/recipes/create/html-or-json"
        
        # Request data structure met json in het data veld als string
        import_data = {
            "html": "",
            "includeTags": True,
            "data": json.dumps(recipe_json),  # JSON als string in data veld
            "includeImages": False
        }
        
        try:
            response = requests.post(url, json=import_data, headers=self.headers)
            response.raise_for_status()
            print(f"Successfully imported recipe: {recipe_json['name']}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error importing recipe: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            print(f"URL used: {url}")
            print(f"Headers: {self.headers}")
            print(f"Data sent: {json.dumps(import_data, indent=2)}")
            return None

    def bulk_import_from_directory(self, directory=None):
        """Import all JSON recipes from a directory"""
        if directory is None:
            directory = os.getenv('RECIPES_DIR', './recipes')
        
        directory = Path(directory)
        if not directory.exists():
            raise ValueError(f"Directory {directory} does not exist")
            
        success = 0
        failed = 0
        failed_recipes = []
        
        print(f"\nImporting recipes from {directory}")
        
        for recipe_file in directory.glob("*.json"):
            print(f"\nProcessing {recipe_file.name}...")
            try:
                with open(recipe_file) as f:
                    recipe_json = json.load(f)
                
                if self.import_recipe(recipe_json):
                    success += 1
                else:
                    failed += 1
                    failed_recipes.append(recipe_file.name)
                
                time.sleep(1)
            
            except Exception as e:
                print(f"Error processing {recipe_file.name}: {str(e)}")
                failed += 1
                failed_recipes.append(recipe_file.name)

        print(f"\nImport completed!")
        print(f"Successfully imported: {success} recipes")
        print(f"Failed to import: {failed} recipes")
        
        if failed_recipes:
            print("\nFailed recipes:")
            for recipe in failed_recipes:
                print(f"- {recipe}")

def main():
    try:
        importer = MealieImporter()
        importer.bulk_import_from_directory()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
