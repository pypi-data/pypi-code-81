import pandas as pd
import click
import requests
import lxml
from bs4 import BeautifulSoup


SLUG_HELP_TEXT = """Slug is <state><year> for assembly election or ls<year> for lok sabha election.

Examples
--------
1. For Tamil Nadu 2021 assembly election the slug is Tamilnadu2021.
2. For Lok Sabha Election 2019 the slug is ls2019.
3. You can also pass a URL for a particular page like https://myneta.info/Puducherry2021/index.php?action=show_candidates&constituency_id=4
"""

def get_url(slug):
    if slug.startswith(('http', 'www')):
        return slug


def show_tables(dfs):
    for df in dfs:
        click.echo(df)
        click.secho('--' * 10)


def format_table(df, output_file):
    df.to_csv(output_file, index=False)
    click.echo(f'Write the table to file {output_file}')


def get_details(body):
    soup = BeautifulSoup(body)
    try:
        return soup.find_all('div', class_='title')[0].h3.contents[0].replace('(', '').split('-')[-1].strip().split(':')
    except:
        return '', ''

class SkipURL(Exception):
    """SkipURL when the no details found
    """


def get_constituency_details(url):
    resp = requests.get(url)
    if resp.ok:
        constituency, district = get_details(resp.content)
        if constituency and district:
            return constituency.title(), district.title()
    raise SkipURL(url)


def insert_candidate_info(picked_df, constituency, district):
    picked_df['Constituency'] = [constituency] * len(picked_df)
    picked_df['District'] = [district] * len(picked_df)
    return picked_df


def perform_for_one_url(url, output_file=None, table_type='', print_tables=False, write_to_file=True):
    try:
        dfs = pd.read_html(url)
    except (lxml.etree.XMLSyntaxError, ValueError):
        click.secho(f'{url} is empty')
        return None
    table_type = table_type.title()
    picked_df = None

    if print_tables:
        show_tables(dfs)
        exit()

    for df in dfs:
        if table_type in df.columns:
            picked_df = df
            break

    if isinstance(picked_df, pd.DataFrame):
        try:
            cons, district = get_constituency_details(url)
            picked_df = insert_candidate_info(picked_df, cons, district)
        except SkipURL as exc:
            click.secho(exc)
            return None

        if write_to_file:
            format_table(picked_df, output_file)
        else:
            return picked_df
    else:
        click.echo('Could find the table type')

    return None


def perform_for_group(slug, output_file, table_type,
                      print_tables, total):
    url = 'https://myneta.info/{slug}/index.php?action=show_candidates&constituency_id={idx}'
    idx, completed = 1, 0

    df = None
    while completed != total:
        full_url = url.format(slug=slug, idx=idx)
        returned_df = perform_for_one_url(url=full_url, output_file=None, write_to_file=False,
                                          table_type=table_type, print_tables=print_tables)
        if isinstance(returned_df, pd.DataFrame):
            completed += 1
            if isinstance(df, pd.DataFrame):
                df = pd.concat([df, returned_df])
            else:
                df = returned_df

        if completed % 10 == 1:
            click.secho(f'Total={total}, completed={completed}')
        idx += 1

    format_table(df, output_file)


@click.command()
@click.argument('slug')
@click.option('-o', '--output-file', required=False, type=click.Path())
@click.option('--table-type', default='')
@click.option('--print-tables', is_flag=True, required=False)
@click.option('--total', type=int)
def main(slug, output_file, table_type, print_tables, total):
    if slug.startswith('http'):
        perform_for_one_url(url=slug, output_file=output_file,
                            table_type=table_type, print_tables=print_tables,
                            write_to_file=True)

    perform_for_group(slug, output_file, table_type=table_type,
                      print_tables=print_tables, total=total)

if __name__ == "__main__":
    main()
