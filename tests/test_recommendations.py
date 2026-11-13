import copy
import json
import tempfile
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from config import config
from modules.api_client import LLMClient
from modules.recommendation_logic import (
    analysis_context,
    load_catalogue,
    request_signature,
    validate_response,
)


class RecommendationTests(unittest.TestCase):
    def setUp(self):
        self.catalogue = load_catalogue()
        self.output = {
            "analysis_summary": "Visible dryness.",
            "products": [
                {
                    "product_id": product_id,
                    "why": "The catalogue lists it as an option for the visible concerns.",
                    "selection_note": "Compare with the other options before choosing.",
                }
                for product_id in ("P08", "P01", "P15", "P18")
            ],
            "routine": {
                "morning": [{"instruction": "Moisturize as directed.", "product_id": None}],
                "evening": [{"instruction": "Follow label directions.", "product_id": "P08"}],
            },
            "tips": ["Introduce products individually."],
            "limitations": "Image observations are uncertain.",
        }

    def test_catalogue(self):
        self.assertGreaterEqual(len(self.catalogue), 20)
        for product in self.catalogue:
            self.assertTrue(product["source_url"].startswith("https://"))
            self.assertTrue(product["benefits"])

    def test_validation(self):
        validated = validate_response(json.dumps(self.output), self.catalogue)
        self.assertEqual(len(validated["products"]), 4)

        for change in ("unknown", "duplicate", "routine", "missing", "too many"):
            with self.subTest(change=change):
                output = copy.deepcopy(self.output)
                if change == "unknown":
                    output["products"][0]["product_id"] = "INVENTED"
                elif change == "duplicate":
                    output["products"][1] = output["products"][0].copy()
                elif change == "routine":
                    output["routine"]["morning"][0]["product_id"] = "P20"
                elif change == "missing":
                    del output["limitations"]
                else:
                    output["products"].append({
                        "product_id": "P20",
                        "why": "Another option.",
                        "selection_note": "Consider as an alternative.",
                    })
                with self.assertRaises(ValueError):
                    validate_response(json.dumps(output), self.catalogue)

    def test_minimized_context(self):
        analysis = {
            "concerns": ["dryness"],
            "skin_condition_description": "Dry appearance",
            "age_estimate": 30,
            "image_name": "private.jpg",
        }
        self.assertEqual(set(analysis_context(analysis)), {"concerns", "skin_condition_description"})
        self.assertNotEqual(
            request_signature(analysis, self.catalogue),
            request_signature({"concerns": ["oil"]}, self.catalogue),
        )

    def test_app_empty_and_mock_api(self):
        with tempfile.TemporaryDirectory() as users_dir, patch.object(config, "USERS_DIR", users_dir), patch.object(
            config, "API_KEY", "test-server-key"
        ):
            app = AppTest.from_file("app.py").run()
            self.assertFalse(app.exception)
            app.button(key="nav_Recommendations").click().run()
            self.assertTrue(any("Start with a profile" in block.value for block in app.markdown))

            app.session_state.user_id = "test-profile"
            app.run()
            self.assertTrue(any("Start with a skin analysis" in block.value for block in app.markdown))

            app.session_state.current_analysis = {
                "concerns": ["Dryness"],
                "skin_condition_description": "Visible dry texture.",
            }
            app.run()
            api_key = next(field for field in app.text_input if field.label == "API key")
            self.assertEqual(api_key.value, "")
            api_key.set_value("test-session-key")
            next(button for button in app.button if button.label == "Save API key").click().run()
            self.assertEqual(config.API_KEY, "test-server-key")

            with patch.object(
                LLMClient, "call_llm", autospec=True,
                return_value={"success": True, "response": json.dumps(self.output)},
            ) as generate:
                next(button for button in app.button if button.label == "Generate Recommendations").click().run()
            self.assertEqual(generate.call_args.args[0].api_key, "test-session-key")
            self.assertFalse(app.exception)
            self.assertEqual(
                [tab.label for tab in app.tabs], ["Product options", "Daily routine", "Tips & cautions"]
            )
            cards = [block.value for block in app.markdown if 'class="recommendation-product-copy"' in block.value]
            self.assertEqual(len(cards), 4)
            self.assertTrue(any("Hyaluronic Acid" in card for card in cards))

            app.session_state.current_analysis = {
                "concerns": ["Oil"],
                "skin_condition_description": "Visible shine.",
            }
            app.run()
            self.assertIsNone(app.session_state.recommendations)


if __name__ == "__main__":
    unittest.main()
