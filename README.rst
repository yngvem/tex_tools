============
Code Printer
============

A couple of home-brewed tex-based tools. The scripts folder contains two utilities, one to generate PDFs from Python files and one to generate PNGs from LaTeX equations.

-------------
Installation:
-------------
Clone this repo, navigate to it in terminal window and run

.. code:: bash

    pip install -e .

----------------
Example scripts:
----------------

**The following script will generate a PDF with all files in tex_tools**

.. code:: bash

    cd scripts
    python code_printer.py python ../src/tex_tools tex_tools --save_pdf true --save_tex true


**The following script will create a PNG with a single equation (note double backslashes):**

.. code:: bash

    cd scripts
    python png_generator.py \frac{1}{2} half.png --dpi 3000
    
**The following script will create a PNG for each equation in the specified JSON file**

.. code:: bash
    cd scripts
    python png_generator.py sag/equations.json sag/output --header-file sag/header.tex --dpi 3000