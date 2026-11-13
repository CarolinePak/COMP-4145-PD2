# modules/skin_analysis.py

import streamlit as st
import json
from datetime import datetime
from modules import ui
from modules.api_client import client_for_session
from prompts.prompt_utils import load_prompt
import uuid
import os
from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError


MAX_IMAGE_PIXELS = 25_000_000

def render():
    ui.heading("Skin Analysis", "Review visible skin patterns from a clear, well-lit photo.", "scan")

    with ui.panel("analysis"):
        photo_col, results_col = st.columns([1, 1.2])
        with photo_col, ui.panel("card"):
            st.header("Your photo")
            _render_photo_controls()
        with results_col, ui.panel("card"):
            st.header("Your results")
            if st.session_state.current_analysis:
                display_results(st.session_state.current_analysis)
            else:
                ui.empty_state(
                    "Ready for your first analysis",
                    "Your scores, visible concerns, and skincare suggestions will appear here.",
                    "scan",
                )


def _render_photo_controls():
    image_source = st.radio("Photo source", ["Upload image", "Take a photo"], horizontal=True)
    using_camera = image_source == "Take a photo"
    if using_camera:
        ui.html(
            '<style>[data-testid="stCameraInput"] video, [data-testid="stCameraInput"] img '
            '{transform: scaleX(-1);}</style>'
        )
        uploaded_file = st.camera_input("Take a face photo")
    else:
        uploaded_file = st.file_uploader(
            "Choose a face image", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
        )

    with st.expander("Tips for a clear photo"):
        st.markdown(
            "- Face the camera directly and keep your entire face in frame.\n"
            "- Use even, natural light and avoid strong shadows.\n"
            "- Use a sharp image without filters or makeup."
        )
    st.caption(
        "When you start an analysis, your photo is sent to the configured AI service. "
        "The original photo is not saved locally."
    )
    if uploaded_file is None:
        return

    valid, error = validate_image(uploaded_file)
    if not valid:
        st.error(error)
        return

    preview = prepare_image_bytes(uploaded_file, mirror_horizontal=using_camera)
    st.image(preview, caption="Selected photo", use_column_width=True)
    if st.button("Analyze photo", type="primary", use_container_width=True):
        analyze_skin(uploaded_file, mirror_horizontal=using_camera)


def validate_image(uploaded_file) -> tuple:
    """
    Validate uploaded image file.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        (is_valid: bool, error_message: str or None)
    """

    from config import config

    # Check file size
    if uploaded_file.size > config.MAX_IMAGE_SIZE:
        size_mb = uploaded_file.size / (1024 * 1024)
        max_mb = config.MAX_IMAGE_SIZE / (1024 * 1024)
        return False, f"File too large ({size_mb:.1f}MB). Maximum size: {max_mb:.1f}MB"

    try:
        image_bytes = uploaded_file.getvalue()
        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()
        with Image.open(BytesIO(image_bytes)) as image:
            if image.format not in {"JPEG", "PNG"}:
                return False, "Invalid image format. Allowed formats: JPG, JPEG, PNG"
            if image.width * image.height > MAX_IMAGE_PIXELS:
                return False, "Image resolution is too large. Maximum: 25 megapixels"
    except (AttributeError, OSError, UnidentifiedImageError):
        return False, "The selected file is not a valid or readable image"

    return True, None


def prepare_image_bytes(uploaded_file, mirror_horizontal: bool = False) -> bytes:
    """Normalize uploaded or camera images to an upright RGB JPEG."""
    with Image.open(BytesIO(uploaded_file.getvalue())) as image:
        image = ImageOps.exif_transpose(image)

        if mirror_horizontal:
            image = ImageOps.mirror(image)

        if image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        ):
            rgba = image.convert("RGBA")
            background = Image.new("RGBA", rgba.size, "white")
            background.alpha_composite(rgba)
            image = background.convert("RGB")
        else:
            image = image.convert("RGB")

        output = BytesIO()
        image.save(output, format="JPEG", quality=90, optimize=True)
        return output.getvalue()


def analyze_skin(uploaded_file, mirror_horizontal: bool = False):
    """
    Perform skin analysis using LLM.

    Args:
        uploaded_file: Streamlit UploadedFile object
    """

    # Check API key
    client = client_for_session()
    if not client.api_key:
        st.error("API key not configured. Add it in Settings to continue.")
        return

    # Show loading state
    with st.spinner("Reviewing your photo. This may take 10–20 seconds."):

        # Normalize uploads and camera captures to JPEG for the vision API.
        try:
            image_bytes = prepare_image_bytes(
                uploaded_file,
                mirror_horizontal=mirror_horizontal,
            )
        except (OSError, UnidentifiedImageError):
            st.error("The selected image could not be processed. Please choose another photo.")
            return

        # Load prompts
        try:
            system_prompt = load_prompt("skin_analysis_system")
            user_prompt = load_prompt("skin_analysis_user")
        except FileNotFoundError as e:
            st.error(f"Prompt template error: {e}")
            return

        # Call LLM API
        result = client.call_with_image(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            image_bytes=image_bytes,
            temperature=0.3,  # Lower for consistent analysis
            max_tokens=1500
        )

        if result["success"]:
            # Parse response
            try:
                analysis_data = parse_analysis_response(result["response"])

                # Add metadata
                analysis_data["timestamp"] = datetime.now().isoformat()
                analysis_data["analysis_id"] = str(uuid.uuid4())
                analysis_data["image_name"] = uploaded_file.name

                # Store in session state
                st.session_state.current_analysis = analysis_data
                st.session_state.analyses.append(analysis_data)

                # Save to file
                save_analysis(analysis_data)

                st.success("Analysis complete.")
                st.rerun()

            except Exception as e:
                st.error(f"Unable to read the analysis results: {str(e)}")

                # Show raw response for debugging
                with st.expander("Technical details"):
                    st.code(result["response"])

        else:
            st.error(f"Analysis failed: {result['error']}")


def parse_analysis_response(response_text: str) -> dict:
    """
    Parse LLM response into structured format.

    Expected LLM response:
    {
        "skin_cleanliness_score": 8,
        "skin_quality_score": 7,
        "age_estimate": 28,
        "skin_condition_description": "...",
        "concerns": ["..."],
        "recommendations": ["..."]
    }

    Args:
        response_text: Raw LLM response

    Returns:
        Parsed dict with structured data

    Raises:
        json.JSONDecodeError: If response is not valid JSON
        ValueError: If required fields are missing
    """

    # Clean response
    response_text = response_text.strip()

    # Remove markdown code blocks
    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "", 1)
    if response_text.startswith("```"):
        response_text = response_text.replace("```", "", 1)
    if response_text.endswith("```"):
        response_text = response_text.rsplit("```", 1)[0]

    # Parse JSON
    data = json.loads(response_text.strip())

    # Validate required fields
    required_fields = [
        "skin_cleanliness_score",
        "skin_quality_score",
        "age_estimate",
        "skin_condition_description"
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Ensure scores are integers in range [0, 10]
    data["skin_cleanliness_score"] = int(max(0, min(10, data["skin_cleanliness_score"])))
    data["skin_quality_score"] = int(max(0, min(10, data["skin_quality_score"])))

    # Ensure age is reasonable
    data["age_estimate"] = int(max(0, min(120, data["age_estimate"])))

    # Ensure lists exist (even if empty)
    if "concerns" not in data:
        data["concerns"] = []
    if "recommendations" not in data:
        data["recommendations"] = []

    return data


def display_results(analysis: dict):
    """Display the latest assessment and next steps."""
    with ui.panel("metrics"):
        for column, label, value in zip(
            st.columns(3),
            ("Cleanliness", "Skin quality", "Estimated age"),
            (
                f"{analysis['skin_cleanliness_score']}/10",
                f"{analysis['skin_quality_score']}/10",
                f"{analysis['age_estimate']} years",
            ),
        ):
            column.metric(label, value)

    st.subheader("Skin condition")
    st.write(analysis["skin_condition_description"])
    for key, title in (("concerns", "Visible concerns"), ("recommendations", "Suggestions")):
        if analysis.get(key):
            st.subheader(title)
            for entry in analysis[key]:
                st.markdown(f"- {entry}")

    st.caption("These AI estimates are for information and do not provide a diagnosis.")
    with st.expander("Assessment details"):
        st.caption(f"Analysis ID: {analysis.get('analysis_id', '—')}")
        st.caption(f"Recorded: {analysis.get('timestamp', '—')}")
    with ui.panel("result-actions"):
        chat_col, routine_col = st.columns(2)
        with chat_col:
            ui.page_button("Discuss results", "Chatbot", key="scan_chat", full=True)
        with routine_col:
            ui.page_button("Explore recommendations", "Recommendations", key="scan_routine", full=True)


def save_analysis(analysis: dict):
    """
    Save analysis to JSON file for history tracking.

    Args:
        analysis: Analysis dict to save
    """

    try:
        from config import config

        # Get user ID (or use 'guest' if not logged in)
        user_id = st.session_state.get("user_id") or "guest"

        # Create user directory
        user_dir = os.path.join(config.ANALYSES_DIR, user_id)
        os.makedirs(user_dir, exist_ok=True)

        # Save as JSON file
        filename = os.path.join(user_dir, f"{analysis['analysis_id']}.json")

        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)

    except Exception as e:
        # Just log the error, don't stop the analysis from displaying
        st.warning(f"Could not save analysis to file: {e}")
        # Analysis still works, just not saved to disk
