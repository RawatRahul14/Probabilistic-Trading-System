# === Python Modules ===
import yaml
from pathlib import Path
from typing import List, Dict, Literal, Any

# === Load YAML files ===
def load_yaml(
        file_path: Literal["config"],
        file_name: str
) -> Dict[str, List[str]]:
    """
    Loads the yaml file's data.

    Args:
        - file_path (Path or str): Path to that folder
        - file_name (str): Name of the file

    returns:
        - data_dict (Dict[str, List[str]]): List of all the components inside the yaml file.
    """
    ## === If any required parameter is missing ===
    missing_params: List[str] = []

    if file_path is None:
        missing_params.append("file_path")

    if file_name is None:
        missing_params.append("file_name")

    if missing_params:
        raise ValueError(
            f"Required parameters missind: {', '.join(missing_params)}"
        )

    ## === Building the file path ===
    path = Path(file_path) / file_name

    try:
        ## === loading data from yaml ===
        with open(path, "rb") as f:
            data_dict = yaml.safe_load(f)

        return data_dict

    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML format in {path}: {e}.")

def save_yaml(
        file_path: Literal["config"],
        file_name: str,
        data: Dict[str, Any]
):
    """
    Saves data in the specific yaml file
    """
    ## === If any required parameter is missing ===
    missing_params: List[str] = []

    if file_path is None:
        missing_params.append("file_path")

    if file_name is None:
        missing_params.append("file_name")

    if data is None:
        missing_params.append("data")

    if missing_params:
        raise ValueError(
            f"Required parameters missind: {', '.join(missing_params)}"
        )
    
    ## === Building the file path ===
    path = Path(file_path) / file_name

    try:
        ## === Write YAML safely ===
        with open(path, "w", encoding = "utf-8") as f:
            yaml.safe_dump(
                data,
                f,
                default_flow_style = False,
                sort_keys = False
            )

    except Exception as e:
        raise RuntimeError(
            f"Failed to save YAML file '{file_name}': {str(e)}"
        )

# === Function to read .md files ===
def read_md(
        file_path: str | Path
) -> str:
    """
    Reads a Markdown (.md) file and returns its content as a string.

    Args:
        file_path (str | Path): Path to the markdown file.

    Returns:
        str: Content of the markdown file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Markdown file not found: {path}")

    if path.suffix.lower() != ".md":
        raise ValueError(f"Expected a .md file, got: {path.suffix}")

    return path.read_text(encoding = "utf-8")