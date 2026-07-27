# Auto-QAPF Plutonic

A simple tool for automatic plutonic rocks classification using QAPF diagram. Great for teaching magmatic rock nomenclature to geology students, but also for a quick but accurate rock identification.

The nomenclature follows the official IUGS guidelines, as provided by [Le Maitre, R. W. (2002)](https://http://dx.doi.org/10.1017/CBO9780511535581), including the **color index prefixes** (i.e., *leuco-* and *mela-*) and **special rock names** (e.g., *trondhjemite*). **Ultramafic** and **gabbroic** rock classification and nomenclature are supported as well.

## Installation

### Windows

Download the dedicated executable for the [latest version](https://github.com/albdag/auto-qapf-plutonic/releases/latest). No installation is required.

### Linux & macOS

> [!IMPORTANT]
> **Requirements**:
>
> * Python 3.12.2
> * Git (required to clone the repository)

1. Clone repository:

   ```Shell
   git clone https://github.com/albdag/auto-qapf-plutonic.git
   cd auto-qapf-plutonic
   ```

   If **Git** is not installed, download the repository as a ZIP file, extract it, and open a terminal in the extracted folder.
2. Create a virtual environment:

   ```Shell
   python -m venv auto-qapf
   ```
3. Activate environment:

   ```Shell
   source .venv/bin/activate
   ```
4. Install dependencies from requirements.txt:

   ```Shell
   pip install -r requirements.txt
   ```
5. Run the Python script

   ```Shell
   python auto_qapf_plutonic.py
   ```

## Citing This Work

If you use this software as part of your research, please cite the [original paper](https://doi.org/10.3301/ROL.2019.51):

> Ortolano, G.; D’Agostino, A.; Visalli, R.; Cirrincione, R. (2019). Plutonic rocks classification: A child’s play. Rendiconti Online della Società Geologica Italiana, 49, 46-54. https://doi.org/10.3301/ROL.2019.51
