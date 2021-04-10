#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/25 15:15
# @Author : 詹荣瑞
# @File : parser_tex.py
# @desc : 本代码未经授权禁止商用
from typing import List
import pyparsing as pp


def command_analyse(str_list: List[str]):
    string = str_list[0]
    if string not in {
        r"\section",
        r"\subsection",
        r"\subsubsection",
        r"\TeX",
        # r"\label",
        r"\textbf",
    }:
        # string = string.replace("\\", r"")
        # return "你或许使用了不支持的命令"
        return ""
    if len(str_list) == 1:
        return string
    else:
        return f"{string}{{{str_list[1]}}}\n"


command_line = pp.Forward()
code_block = pp.Forward()

empty = pp.empty
line_split = r"\\"
formula = pp.Combine("$"+pp.Regex("[^$]+")+"$")
word = pp.Regex(r"[|!-?A-Z^-z\u4e00-\u9fa5]+")
command = pp.Word("\\", pp.alphas, 2)
paragraph = pp.ZeroOrMore(line_split | formula | command_line | command | code_block | word)
code_block <<= pp.Suppress("{") + paragraph + pp.Suppress("}")

command_option = pp.Combine("[" + pp.Word(pp.alphas + "!") + "]") | empty
command_line <<= command + pp.ZeroOrMore(code_block) + command_option
command_line.addParseAction(command_analyse)
paragraph.addParseAction(lambda x: " ".join(x))


# "\n".join(x)


def parse_tex(string):
    # print(paragraph.parseString(string)[0], type(paragraph.parseString(string)[0]))
    return paragraph.parseString(string)[0].replace("&", r"\,")


if __name__ == '__main__':
    test_string = r"""\documentclass{article} 
\title{Bone\TeX{} Code 使用手册} 
\author{Bone\TeX} 
\usepackage{ctex} 
\usepackage{multirow} 
\usepackage{graphicx} 
\begin{document}

  \maketitle 
  \section{模板} 
  \label{sec:2754909747400} 
  \subsection{示例} 
  \label{sec:2754909747272} 
  \begin{table}[h!t]
    \centering
    \caption{乘法口诀表}
    \begin{tabular}{*{6}{l}}
        $1\times 1=1$\\
    $2\times 1=2$&$2\times 2=4$\\
    $3\times 1=3$&$3\times 2=6$&$3\times 3=9$\\
    $4\times 1=4$&$4\times 2=8$&$4\times 3=12$&$4\times 4=16$\\
    $5\times 1=5$&$5\times 2=10$&$5\times 3=15$&$5\times 4=20$&$5\times 5=25$\\
    
    \end{tabular}
  \end{table}


  \section{内置模块} 
  \label{sec:2754909816328} 
  \subsection{示例} 
  \label{sec:2754909817096} 
  \begin{table}[htbp]
    \centering 
    \caption{乘法口诀表} 
    \label{tab:2754909817608} 
    \begin{tabular}{|c|c|c|c|c|}
      \hline
      $1\times 1=1$\\
      \hline
      $2\times 1=2$ & $2\times 2=4$\\
      \hline
      $3\times 1=3$ & $3\times 2=6$ & $3\times 3=9$\\
      \hline
      $4\times 1=4$ & $4\times 2=8$ & $4\times 3=12$ & $4\times 4=16$\\
      \hline
      $5\times 1=5$ & $5\times 2=10$ & $5\times 3=15$ & $5\times 4=20$ & $5\times 5=25$\\
      \hline
    \end{tabular} 
  \end{table} 

\end{document} """
    print(parser_tex(test_string))
