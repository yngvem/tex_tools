import argparse
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import jinja2

from tex_tools.utils import generate_pdf, get_template


def parse_filename(path):
    path = Path(path)
    return path.stem.replace('_', ' ').capitalize()


def load_file(path):
    with Path(path).open('r') as f:
        return parse_filename(path), f.read()


def load_files(folder):
    return dict(load_file(python_file) for python_file in Path(folder).glob('*.py'))


def render_tex(template_path, template_name, code_blocks):
    template = get_template(template_path, template_name)
    return template.render(content=code_blocks)


def main(input_data, out_file):
    input_data = Path(input_data)
    if input_data.is_file():
        name, content = load_file(input_data)
        code_blocks = {name: content}
    elif input_data.is_dir():
        code_blocks = load_files(input_data)
    else:
        raise ValueError('input_data should be file or directory')

    if len(code_blocks) == 0:
        raise ValueError('The input folder has no `.py` files.')

    template_path = Path(__file__).parent 
    template_name = 'template.tex'
    tex = render_tex(template_path, template_name, code_blocks)
    generate_pdf(tex, out_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path')
    parser.add_argument('output_path')

    args = parser.parse_args()

    main(args.input_path, args.output_path)
