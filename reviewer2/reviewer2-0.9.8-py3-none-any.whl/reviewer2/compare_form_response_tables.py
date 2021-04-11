import argparse
import pandas as pd

EXPECTED_COLUMNS = {"Path", "Verdict", "Confidence"}
HIGH_CONFIDENCE = "high"

def parse_args():
    p = argparse.ArgumentParser(description="Check concordance between two form response tables created by 2 users "
        "reviewing the same images. Rows in the two tables are matched by their same Path column.")
    p.add_argument("-s1", "--suffix1", "Suffix to append to column names from table1", default="1")
    p.add_argument("-s2", "--suffix2", "Suffix to append to column names from table2", default="2")
    p.add_argument("-o", "--output-tsv", "Path of output .tsv", default="combined.tsv")
    p.add_argument("table1", "Path of form response table .tsv")
    p.add_argument("table2", "Path of form response table .tsv")
    args = p.parse_args()

    try:
        df1 = pd.read_table(args.table1)
    except Exception as e:
        p.error(f"Error parsing {args.table1}: {e}")

    try:
        df2 = pd.read_table(args.table2)
    except Exception as e:
        p.error(f"Error parsing {args.table2}: {e}")

    if EXPECTED_COLUMNS - set(df1.columns):
        p.error(f"{args.table1} is missing columns: " + ", ".join(EXPECTED_COLUMNS - set(df1.columns)))

    if EXPECTED_COLUMNS - set(df2.columns):
        p.error(f"{args.table2} is missing columns: " + ", ".join(EXPECTED_COLUMNS - set(df2.columns)))

    if len(df1) == 0:
        p.error(f"{args.table1} is empty")

    if len(df2) == 0:
        p.error(f"{args.table2} is empty")

    df1 = df1.set_index("Path")
    df2 = df2.set_index("Path")

    if len(set(df1.index) & set(df2.index)) == 0:
        p.error(f"{args.table1} Path column values have 0 overlap with {args.table2} Path column values. Tables can only "
                f"be combined if they have the same Paths.")

    return args, df1, df2

def compute_concordance_columns(suffix1, suffix2):
    verdict_column1 = f"Verdict{suffix1}"
    verdict_column2 = f"Verdict{suffix2}"
    confidence_column1 = f"Confidence{suffix1}"
    confidence_column2 = f"Confidence{suffix2}"

    def compute_discordance_columns(row, score_column="Discordance Score", text_column="Discordance Text"):
        if not row[verdict_column1] or not row[verdict_column2]:
            return row

        if row[verdict_column1] == row[verdict_column2]:
            # same verdict
            row[score_column] = 0
            row[text_column] = "same verdict"
            if row[confidence_column1] and row[confidence_column2]:
                if row[confidence_column1] == row[confidence_column2]:
                    row[score_column] = 0
                    row[text_column] = "same verdict, same confidence"
                else:
                    row[score_column] = 1
                    row[text_column] = "same verdict, different confidence"
        else:
            # different verdicts
            row[score_column] = 2
            row[text_column] = "different verdict"
            if row[confidence_column1] or row[confidence_column2]:
                if row[confidence_column1] == HIGH_CONFIDENCE and row[confidence_column2] == HIGH_CONFIDENCE:
                    row[score_column] = 4
                    row[text_column] = "different verdict, both high confidence"
                elif row[confidence_column1] == HIGH_CONFIDENCE or row[confidence_column2] == HIGH_CONFIDENCE:
                    row[score_column] = 3
                    row[text_column] = "different verdict, one high confidence"
                else:
                    row[score_column] = 2
                    row[text_column] = "different verdict, zero high confidence"

        return row


def main():
    args, df1, df2 = parse_args()
    df_joined = df1.join(df2, lsuffix=args.suffix1, rsuffix=args.suffix2).reset_index()

    #  compute concordance
    df_joined = df_joined.apply(compute_concordance_columns, axis=1)

    df_joined.to_csv(args.output_tsv, header=True, sep="\t", index=False)
    print(f"Wrote {len(df_joined)} rows to {args.output_tsv}")


if __name__ == "__main__":
    main()
