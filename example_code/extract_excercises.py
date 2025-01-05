preamble=r"""\documentclass[14pt]{extarticle}
\usepackage{graphicx} % Required for inserting images
% \usepackage{fullpage}
\usepackage[left=1cm, right=1cm]{geometry}

\usepackage{listings}
\usepackage[dvipsnames]{xcolor}
\usepackage{amsmath}
\usepackage{mdframed}

\newcommand{\ls}[1]{\lstinline{#1}}
\newcommand{\dd}{\ensuremath{\mathrm{d}}}
\newcommand{\diff}[2]{\ensuremath{\frac{\dd {#1}}{\dd {#2}}}}
\newcommand{\bv}[1]{\ensuremath{\mathbf{#1}}}


\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}
\definecolor{exercise}{gray}{1}

\newcounter{exercise}
\newenvironment{exercise}[1][]%
    {\refstepcounter{exercise}%
    \par\noindent%
    \textbf{Exercise~\theexercise.} #1 \rmfamily}%
    {\medskip}


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
    tabsize=2
}

\lstset{style=py}

\title{NOFY080 exercises}
\author{Emil Varga}
\date{\today}

\begin{document}

\maketitle"""

postamble = r"\end{document}"

import os
here = os.path.dirname(__file__)
with open(os.path.join(here, "../main.tex"), 'r') as file,\
     open(os.path.join(here, "../exercises.tex"), 'w') as ex:
    print(ex)
    in_ex = False
    ex_lines = []
    ex.write(preamble)
    exercises = 0
    for line in file:
        if r"\BEGIN{EXERCISE}" in line.upper():
            in_ex = True
            exercises += 1
        elif r"\END{EXERCISE}" in line.upper():
            in_ex = False
            ex_lines.append(line)
            ex.write("".join(ex_lines))
            ex_lines = []
        
        if in_ex:
            ex_lines.append(line)
    ex.write(postamble)
    print(f"Found {exercises} exercises.")