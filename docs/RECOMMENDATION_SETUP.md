# Catalogue-based Recommendations

## Delivered
- 20 English product records in `data/products.json`, summarized from the linked official US brand pages. Catalogue matching tags are editorial, not diagnoses. Ingredients are key ingredients, not exhaustive INCI lists. Regional formulas may differ.
- `modules/recommendation_logic.py`: reads the catalogue, minimizes analysis context and validates AI output.
- `modules/recommendations.py`: English product cards, morning/evening routine, tips, catalogue browser and error states.
- Updated recommendation prompt and app routing.
- Uses the existing API Settings and API client configuration. No changes to API client, skin analysis or chatbot are included.

## How it works
Complete Skin Analysis, open Recommendations, save your API key in the sidebar and click Generate Recommendations. The configured API receives only concerns, skin description and catalogue data. No additional image, age or score is sent for recommendations. AI chooses 0–3 IDs without category quotas and generates reasons and routines. The app rejects unknown/duplicate IDs and routine references to unselected products. Names, benefits, ingredients and links displayed on product cards come directly from the catalogue.

Generic routine steps (including sunscreen) may appear without a catalogue product. Similar options are alternatives. Prompt constraints reduce unsupported claims but do not guarantee all generated prose is factually grounded; inspect results during live testing.

## Catalogue limitations
The dataset covers three brands and is weighted toward hydration. It is a prototype catalogue, not a market-wide ranking. Detailed usage is marked explicitly: when not transcribed, AI must refer to the current label and must not invent dosage. Cautions are concise and not exhaustive; retain official links. Do not infer allergies or confirmed skin type from a face photo.

## Run
Use Python with the dependencies from requirements.txt, then:

    python -m streamlit run app.py

Use the model and endpoint supported by your institution. The inherited model name has not been verified against the live service. No API key is included.

## Verification
Run from the project folder:

    python -m unittest discover -s tests -v

Four tests cover catalogue integrity, invalid IDs/response structures, minimized context and Streamlit routing/rendering with a mocked API response plus stale-result invalidation. Live API and cloud persistence are not tested. Automated response validation checks structure and product references; it is not a clinical or semantic review.

## Upload to GitHub
Create `feature/product-recommendation` from the latest main branch. Upload the files in the change bundle, preserving paths, and open a pull request. Review differences first if teammates updated app.py, chatbot.py or skin_analysis.py after the provided ZIP. Do not replace their newer work wholesale. Do not upload .env, secrets, API keys, local analysis records or virtual environments.

The change bundle is based on ZIP commit e4250e70376616b4c0d3f0642984ab1ff78279fd, not a live checkout. This project retains the existing multi-file layout.
