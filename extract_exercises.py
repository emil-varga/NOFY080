import re
import os

preamble = r"""\documentclass[12pt]{article}
\usepackage{graphicx} % Required for inserting images
\usepackage[left=2cm, right=2cm, top=3cm, bottom=3cm]{geometry}
\usepackage{hyperref}
\usepackage{url}
\usepackage[titles]{tocloft}
\usepackage{amsmath}

\usepackage{listings}
\usepackage[dvipsnames]{xcolor}
%\usepackage{amsmath}
\usepackage{mdframed}

\graphicspath{{figures/}}

\renewcommand{\lstlistlistingname}{Code Snippets}

\newcommand{\dd}{\ensuremath{\mathrm{d}}}
\newcommand{\diff}[2]{\ensuremath{\frac{\dd {#1}}{\dd {#2}}}}
\newcommand{\bv}[1]{\ensuremath{\mathbf{#1}}}
\newcommand{\ls}[1]{\lstinline{#1}}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}
\definecolor{exercise}{gray}{0.9}
\definecolor{SIM}{cmyk}{0.1, 0, 0, 0}

\newcounter{exercise}
\newenvironment{exercise}[1][]%
    {\refstepcounter{exercise}%
    \counterwithin*{exercise}{section}%
    \begin{mdframed}[backgroundcolor=exercise,linecolor=white]%
    \textbf{Exercise~\thesection.\theexercise.} #1 \rmfamily}%
    {\medskip\end{mdframed}}

\newcommand{\listsyntax}{Python Language Intermezzos}
\newlistof{intermezzos}{synt}{\listsyntax}
\newcounter{syntax}
\newenvironment{syntax}[1][Syntax]%
    {\refstepcounter{syntax}%
    \addcontentsline{synt}{intermezzos}{#1}
    \begin{mdframed}[backgroundcolor=SIM,linecolor=white]%
    \textbf{Intermezzo~\thesyntax:} \textit{#1}}%
    {\medskip\end{mdframed}}

\lstdefinestyle{py}{
    backgroundcolor=\color{backcolour},
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    keepspaces=true,
    numbers=left,
    numbersep=5pt,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=2,
    language=Python
}
\lstset{style=py}

\begin{document}


"""

def extract_exercises(file_contents):
    """
    Extracts all exercise environments from a string of LaTeX content.
    """
    return re.findall(r'\\begin{exercise}(.*?)\\end{exercise}', file_contents, re.DOTALL)

def main():
    """
    Main function to extract exercises from all .tex files and save them.
    """
    tex_files = [
        "/home/emil/programming/NOFY080/notes/sections/section_01_setting_up_the_environment.tex",
        "/home/emil/programming/NOFY080/notes/sections/section_02_python_basics.tex",
        "/home/emil/programming/NOFY080/notes/sections/section_03_numpy_scipy_matplotlib.tex",
        "/home/emil/programming/NOFY080/notes/sections/section_04_least_squares_fitting_and_interpolation.tex",
        "/home/emil/programming/NOFY080/notes/sections/section_05_digital_signal_processing.tex",
        "/home/emil/programming/NOFY080/notes/sections/section_06_communication_with_instruments.tex",
        "/home/emil/programming/NOFY080/notes/sections/section_07_parallel_execution.tex",
        "/home/emil/programming/NOFY080/notes/sections/section_08_solutions_of_differential_equations.tex",
        "/home/emil/programming/NOFY080/notes/sections/section_09_what_didnt_fit.tex",
        "/home/emil/programming/NOFY080/notes/sections/appendix.tex",
    ]

    all_exercises = []
    for file_path in tex_files:
        all_exercises.append([])
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            exercises = extract_exercises(content)
            if exercises:
                all_exercises[-1].extend(exercises)

    output_content = ""
    for i, exercises in enumerate(all_exercises):
        output_content += fr"\section{{Exercises from chapter {i+1}}}" + "\n\n"
        for exercise in exercises:
            output_content += fr"\begin{{exercise}} % Exercise {i+1}" + "\n"
            output_content += exercise.strip() + "\n"
            output_content += r"\end{exercise}" + "\n\n"

    with open("/home/emil/programming/NOFY080/exercises.tex", 'w', encoding='utf-8') as f:
        f.write(preamble + output_content + r"\end{document}")

if __name__ == "__main__":
    main()
