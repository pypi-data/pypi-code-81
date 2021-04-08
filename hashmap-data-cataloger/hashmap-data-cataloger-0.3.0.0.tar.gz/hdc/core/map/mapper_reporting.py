#  Copyright © 2020 Hashmap, Inc
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from pathlib import Path
from string import Template

import pandas as pd
from markdown import Markdown

import hdc.utils.markdown_utils as mdutils


def build_report_from_dataframe(df_catalog: pd.DataFrame, output_file, na='-'):
    md = Markdown(extensions=['tables'])
    md_text = generate_report_content(df_catalog, na)

    base_html = Template("""<!DOCTYPE html> 
                         <html> 
                             <head>
                                 <style> 
                                    $css_style 
                                 </style>
                             </head>
                             <body>
                                 $html_body
                             </body>
                         </html>""")

    base_style = """
                    body {
                            background-color: white;
                            font-family: Tahoma, Verdana, sans-serif;
                        }
                    h1   {color: blue;}
                    h2   {color: red;}
                    p    {
                        color: black;
                        font-size: 20px;
                    }
                    table, td, th {
                      border: 1px solid black;
                    }
                    table {
                      border-collapse: collapse;
                      width: 100%;
                    }
                    th {
                        height: 70px;
                        font-size: 15px
                    }
                """
    with open(Path.cwd() / f"{output_file}.html", 'w') as fout:
        fout.writelines(base_html.substitute(html_body=md.convert(md_text),
                                             css_style=base_style))


def generate_report_content(df_catalog: pd.DataFrame, na):
    report = [mdutils.header("Table Report", 1)]

    table_group = df_catalog.groupby(['DATABASE NAME', 'SCHEMA NAME', 'TABLE NAME'])

    for group_name, group_df in table_group:
        group_df['ACTION'] = group_df['TARGET DATA TYPE'].map(lambda val: 'DROPPED' if val.strip() == na else 'MAPPED')
        report.append(mdutils.header(group_name[2].title(), 2))
        report.append(mdutils.blockquote(mdutils.join_with_newline([
            f"{mdutils.bold('Source')} : {mdutils.backtics(f'{group_name[0].upper()}.{group_name[1].upper()}.{group_name[2].upper()}')} "
            f"{mdutils.emsp()}|{mdutils.emsp()} "
            f"{mdutils.bold('Target')} : {mdutils.backtics(f'{group_name[0].upper()}.{group_name[1].upper()}.{group_name[2].upper()}')}",
            "",
            mdutils.table(group_df[['COLUMN NAME', 'SOURCE DATA TYPE', 'TARGET DATA TYPE', 'ACTION']])
        ])))

    return mdutils.join_with_newline(report)
