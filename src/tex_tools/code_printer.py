import argparse
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from .utils import generate_pdf, get_template


DEFAULT_TEMPLATE_PATH = Path(__file__).parent
DEFAULT_TEMPLATE_NAME = "code_template.tex"


def render_code_to_tex(
    language,
    code_blocks,
    template_path=DEFAULT_TEMPLATE_PATH,
    template_name=DEFAULT_TEMPLATE_NAME,
):
    """

    Arguments
    ---------
    language : str
        Name of language supported by listings
    code_blocks : Dict[str, str]
        Name of section and code to format in that section
    template_path : str
        Path to folder containing a jinja template.
    template_name : str
        Name of jinja template.
    
    Returns
    -------
    str
        LaTeX source code
    """
    if template_path is None:
        template_path = DEFAULT_TEMPLATE_PATH
    if template_name is None:
        template_name = DEFAULT_TEMPLATE_NAME
    
    template = get_template(template_path, template_name)
    return template.render(language=language, content=code_blocks)
