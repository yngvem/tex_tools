import argparse
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import jinja2

from tex_tools.code_printer import render_code_to_tex
from tex_tools.utils import generate_pdf, get_template

LANGUAGE_INFO = {
    "fortran": {
        "file_pattern": "*.f"
    },
    "python": {
        "file_pattern": "*.py"
    },
    "c": {
        "file_pattern": "*.[ch]"
    },
}


def load_file(path, name_formatter):
    with Path(path).open('r') as f:
        return name_formatter(path), f.read()


def load_files(folder, glob_pattern, name_formatter):
    return dict(
        load_file(python_file, name_formatter)
        for python_file in Path(folder).glob(glob_pattern)
    )


def main(input_path, output_path, language, save_pdf, save_tex):
    language_data = LANGUAGE_INFO[language]
    glob_pattern = language_data["file_pattern"]
    name_formatter = language_data.get("name_formatter", str)

    input_data = Path(input_path)
    if input_data.is_file():
        name, content = load_file(input_path, name_formatter)
        code_blocks = {name: content}
    elif input_data.is_dir():
        code_blocks = load_files(input_path, glob_pattern, name_formatter)
    else:
        raise ValueError('input_path should be file or directory')

    if len(code_blocks) == 0:
        raise ValueError(f'The input folder has no files matching the `{glob_pattern}` pattern.')

    template_path = language_data.get("template_parent", None)
    template_name = language_data.get("template_name", None)
    tex = render_code_to_tex(language, code_blocks, template_path, template_name)
    if save_tex:
        with open(f'{output_path}.tex', 'w') as f:
            f.write(tex)
    if save_pdf:
        generate_pdf(tex, f'{output_path}.pdf')


if __name__ == "__main__":
    def str2bool(v):
        # Taken from: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser = argparse.ArgumentParser(description="Program to format code into PDFs using LaTeX")
    supported_languages = set(LANGUAGE_INFO)
    parser.add_argument(f'language', help="One of these strings: {supported_languages}")

    parser.add_argument('input_path', help="Path to single file or folder")
    parser.add_argument('output_path', help="Path to output file (without extension)")
    parser.add_argument('--save_tex', help="Whether to save the generated tex sourcecode", type=str2bool, default="False")
    parser.add_argument('--save_pdf', help="Whether to save compile a PDF", type=str2bool, default="True")

    args = parser.parse_args()

    main(
        input_path=args.input_path,
        output_path=args.output_path,
        language=args.language,
        save_pdf=args.save_pdf,
        save_tex=args.save_tex
    )
