# Import PDF Recipes to Mealie

Unfortunately, this is a somewhat daunting task.  Hopefully you're PDFs have text layers and you are ready for a little bit of manual work.

The solution I found helped me import ~150 recipes into Mealie with minimal editing.

## Step 1

Generate the PDFs using [fabric-ai](https://github.com/danielmiessler/fabric/) and poppler's pdftotext (replace <MODEL> with your LLM):
```
for FILENAME in ./pdfs/*.pdf; do FILENAME=$(echo $FILENAME | sed -e 's/\.\/pdfs\///g' | sed -e 's/\.pdf//g'); pdftotext pdfs/$FILENAME.pdf - | fabric -p ./recipe.md -m '<MODEL>' | grep -v '```' > recipes/$FILENAME.json; done
```

## Step 2

Import the json files (Make sure to set MEALIE_API_KEY and the url variable in the script):
```
python3 import.py
```

## Step 3

Rinse and repeat, making edits or re-generating JSON recipes.
