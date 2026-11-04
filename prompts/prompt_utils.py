# prompts/prompt_utils.py

import os

PROMPTS_DIR = os.path.dirname(__file__)

def load_prompt(prompt_name: str) -> str:
    """
    Load prompt template from file.

    Args:
        prompt_name: Name of prompt file (without .txt extension)

    Returns:
        Prompt text content

    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """

    prompt_file = os.path.join(PROMPTS_DIR, f"{prompt_name}.txt")

    if not os.path.exists(prompt_file):
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read().strip()


def save_prompt(prompt_name: str, content: str):
    """
    Save prompt template to file.

    Args:
        prompt_name: Name of prompt file (without .txt extension)
        content: Prompt text content
    """

    prompt_file = os.path.join(PROMPTS_DIR, f"{prompt_name}.txt")

    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(content)


def list_prompts() -> list:
    """
    List all available prompt templates.

    Returns:
        List of prompt names (without .txt extension)
    """

    prompts = []

    for filename in os.listdir(PROMPTS_DIR):
        if filename.endswith('.txt'):
            prompts.append(filename[:-4])  # Remove .txt

    return sorted(prompts)
