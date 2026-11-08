# modules/skin_analysis.py

import streamlit as st
import json
from datetime import datetime
from modules.api_client import llm_client
from prompts.prompt_utils import load_prompt
import uuid
import os
from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError


MAX_IMAGE_PIXELS = 25_000_000

def render():
    """
    Render the Skin Analysis page.
    Main interface for uploading and analyzing skin images.
    """

    st.title("🔬 AI-Powered Skin Analysis")
    st.markdown("Upload a clear face photo for comprehensive skin quality assessment.")

    # Create two columns: left for upload, right for results
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📸 Upload Image")

        image_source = st.radio(
            "Image source",
            ["Upload Image", "Take a Photo"],
            horizontal=True,
            help="Choose an existing photo or use your device camera.",
        )

        if image_source == "Upload Image":
            uploaded_file = st.file_uploader(
                "Choose a face image",
                type=["jpg", "jpeg", "png"],
                help="Upload a clear, well-lit photo of your face",
                label_visibility="collapsed"
            )
        else:
            # Mirror the live camera and captured preview like a front-facing camera.
            st.markdown(
                """
                <style>
                div[data-testid="stCameraInput"] video,
                div[data-testid="stCameraInput"] img {
                    transform: scaleX(-1);
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            uploaded_file = st.camera_input(
                "Take a face photo",
                help="Your browser may ask for camera permission.",
            )

        st.caption(
            "Privacy: the selected photo is sent to the configured AI service "
            "for analysis. This application does not save the original photo locally."
        )

        if uploaded_file is not None:
            # Validate image
            is_valid, error_msg = validate_image(uploaded_file)

            if not is_valid:
                st.error(f"❌ {error_msg}")
            else:
                # Display image
                preview_bytes = prepare_image_bytes(
                    uploaded_file,
                    mirror_horizontal=image_source == "Take a Photo",
                )
                st.image(preview_bytes, caption="Selected Image", width="stretch")

                # Show file info
                st.caption(f"📄 {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")

                # Analyze button
                if st.button("🔍 Analyze Skin", type="primary", use_container_width=True):
                    analyze_skin(
                        uploaded_file,
                        mirror_horizontal=image_source == "Take a Photo",
                    )
        else:
            # Show placeholder
            if image_source == "Upload Image":
                st.info("👆 Please upload an image to begin analysis")
            else:
                st.info("📷 Allow camera access and take a photo to begin analysis")

            # Sample instructions
            with st.expander("📋 Photo Guidelines"):
                st.markdown("""
                For best results, ensure your photo:
                - Shows your full face clearly
                - Is well-lit (natural lighting preferred)
                - Is front-facing (not angled)
                - Has a clean face (no makeup for accurate analysis)
                - Is in focus (not blurry)
                """)

    with col2:
        st.subheader("📊 Analysis Results")

        # Display results if available
        if st.session_state.current_analysis:
            display_results(st.session_state.current_analysis)
        else:
            st.info("Results will appear here after analysis")


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
    from config import config
    if not config.API_KEY:
        st.error("❌ API key not configured. Please add your API key in the sidebar settings.")
        return

    # Show loading state
    with st.spinner("🔬 Analyzing your skin... This may take 10-20 seconds."):

        # Normalize uploads and camera captures to JPEG for the vision API.
        try:
            image_bytes = prepare_image_bytes(
                uploaded_file,
                mirror_horizontal=mirror_horizontal,
            )
        except (OSError, UnidentifiedImageError):
            st.error("❌ The selected image could not be processed. Please choose another photo.")
            return

        # Load prompts
        try:
            system_prompt = load_prompt("skin_analysis_system")
            user_prompt = load_prompt("skin_analysis_user")
        except FileNotFoundError as e:
            st.error(f"❌ Prompt template error: {e}")
            return

        # Call LLM API
        result = llm_client.call_with_image(
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

                st.success("✅ Analysis complete!")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Failed to parse analysis results: {str(e)}")

                # Show raw response for debugging
                with st.expander("🐛 Debug Info - Raw Response"):
                    st.code(result["response"])

        else:
            st.error(f"❌ Analysis failed: {result['error']}")


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
    """
    Display analysis results in structured UI.

    Args:
        analysis: Parsed analysis dict
    """

    # KPI Cards
    st.markdown("### 📈 Key Metrics")

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        score = analysis['skin_cleanliness_score']
        st.metric(
            label="Skin Cleanliness",
            value=f"{score}/10",
            help="Overall cleanliness and clarity of skin"
        )
        # Color-coded emoji
        if score >= 8:
            st.success("Excellent! ✨")
        elif score >= 6:
            st.info("Good! 👍")
        else:
            st.warning("Needs improvement 💪")

    with metric_col2:
        score = analysis['skin_quality_score']
        st.metric(
            label="Skin Quality",
            value=f"{score}/10",
            help="Overall health and condition of skin"
        )
        if score >= 8:
            st.success("Excellent! ✨")
        elif score >= 6:
            st.info("Good! 👍")
        else:
            st.warning("Needs improvement 💪")

    with metric_col3:
        st.metric(
            label="Estimated Age",
            value=f"{analysis['age_estimate']} years",
            help="AI-estimated age based on skin condition"
        )

    # Progress bars
    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Cleanliness Score**")
        st.progress(analysis['skin_cleanliness_score'] / 10)

    with col_b:
        st.markdown("**Quality Score**")
        st.progress(analysis['skin_quality_score'] / 10)

    # Detailed Description
    st.markdown("---")
    st.markdown("### 📝 Skin Condition Analysis")
    st.write(analysis['skin_condition_description'])

    # Concerns (if any)
    if analysis.get('concerns'):
        st.markdown("---")
        st.markdown("### ⚠️ Identified Concerns")
        for concern in analysis['concerns']:
            st.markdown(f"- {concern}")

    # Quick Recommendations (if any)
    if analysis.get('recommendations'):
        st.markdown("---")
        st.markdown("### 💡 Quick Recommendations")
        for rec in analysis['recommendations']:
            st.markdown(f"- {rec}")

    # Action Buttons
    st.markdown("---")
    st.markdown("### 🎯 Next Steps")

    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if st.button("💬 Discuss with AI Assistant", use_container_width=True):
            st.info("Switch to 'Chatbot' page in the sidebar to discuss your results!")

    with btn_col2:
        if st.button("💄 Get Product Recommendations", use_container_width=True):
            st.info("Switch to 'Recommendations' page in the sidebar!")

    # Analysis metadata
    st.markdown("---")
    st.caption(f"Analysis ID: {analysis['analysis_id']}")
    st.caption(f"Performed: {datetime.fromisoformat(analysis['timestamp']).strftime('%B %d, %Y at %H:%M:%S')}")


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
        st.warning(f"⚠️ Could not save analysis to file: {e}")
        # Analysis still works, just not saved to disk
