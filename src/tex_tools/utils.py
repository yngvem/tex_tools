import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import jinja2
from wand.image import Image

__all__ = ["get_template", "generate_pdf", "generate_png"]


def get_template(template_path, template_name):
    r"""Jinja2 template on the format described here: http://akuederle.com/Automatization-with-Latex-and-Python-2

    Example template

    .. code:: tex
    
        %# Print header
        \BLOCK{ if header in content }
            \VAR{ content.header }
        \BLOCK{ endif }

        %# Print body
        \BLOCK{ for paragraph in content.body }
            \VAR{ paragraph }
        \BLOCK{ endif }
    
    Arguments
    ---------
    template_path : str or Path
        Folder that the template lies in
    template_name : str
        Name of template to load
    """
    environment = jinja2.Environment(
        block_start_string=r'\BLOCK{',
        block_end_string='}',
        variable_start_string=r'\VAR{',
        variable_end_string='}',
        comment_start_string=r'\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(str(template_path))
    )
    return environment.get_template(template_name)


def generate_pdf(tex_content, out_file):
    """Compile a string containing LaTeX source code to PDF.
    """
    out_file = Path(out_file)
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        tex_file = tmpdir/f'{out_file.stem}.tex'

        with tex_file.open('w') as f:
            f.write(tex_content)

        p = subprocess.run(['pdflatex', '-interaction', 'nonstopmode', f'-output-directory={tmpdir}', tex_file.name])

        shutil.copy(tmpdir/f'{tex_file.stem}.pdf', out_file)


def generate_png(tex_content, out_file, dpi=300):
    """Compile a string containing LaTeX source code to a PNG.
    """
    out_file = Path(out_file)
    with TemporaryDirectory() as tempdir:
        tempdir = Path(tempdir)
        pdf_file = tempdir / f"{out_file.stem}.pdf"
        generate_pdf(tex_content, pdf_file)
        
        with Image(filename=pdf_file, resolution=dpi) as source:
            source.trim()
            source.save(filename=str(out_file))
