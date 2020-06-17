import argparse
import json
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import jinja2

from tex_tools import generate_pdf, generate_png, get_template


def render_tex(template_path, template_name, equation, header, header_file):
    template = get_template(template_path, template_name)
    return template.render(equation=equation, header=header, header_file=header_file)


def main(equation, out_file, dpi, header, header_file):
    template_path = Path(__file__).parent
    template_name = "png_template.tex"
    out_file = Path(out_file)

    if Path(equation).is_file():
        out_file.mkdir(parents=True, exist_ok=True)
        with Path(equation).open("r") as f:
            equations = json.load(f)

        for filename, equation in equations.items():
            tex = render_tex(
                template_path,
                template_name,
                equation,
                header=header,
                header_file=header_file,
            )
            generate_png(tex, out_file/filename, dpi=dpi)
    else:
        out_file.parent.mkdir(parents=True, exist_ok=True)
        tex = render_tex(
            template_path,
            template_name,
            equation,
            header=header,
            header_file=header_file,
        )
        generate_png(tex, out_file, dpi=dpi)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("equation")
    parser.add_argument("output_path")
    parser.add_argument("--dpi", default=300, type=int)
    parser.add_argument("--header", default=None)
    parser.add_argument("--header-file", default=None)

    args = parser.parse_args()

    main(args.equation, args.output_path, args.dpi, args.header, args.header_file)
