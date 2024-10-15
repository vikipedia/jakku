"""Compares csv files from newdir to csv files in olddir
python results_match.py newdir olddir
This is utility useful for rumi results. It uses some io framwork from
rumi, so it needs rumi installation to use this script.
"""
import pandas as pd
import numpy as np
import os
import sys
from rumi.io import utilities
from pandas.api.types import is_numeric_dtype

from contextlib import redirect_stdout
import io


def get_csvs(root):
    def csvs():
        for base, dirs, files in os.walk(root):
            yield from [os.path.join(base, f) for f in files if f.endswith(".csv")]

    return {os.path.basename(f): f for f in csvs()}


def get_index_cols(df):
    cols = utilities.get_all_structure_columns(df)
    numeric_cols = [c for c in df.columns if is_numeric_dtype(
        df[c]) and c not in cols]
    rest = [c for c in df.columns if c not in cols and c not in numeric_cols]

    return cols + rest, numeric_cols


def main(directory1, directory2):
    files1 = get_csvs(directory1)
    files2 = get_csvs(directory2)
    for f in files1:
        if f not in files2:
            print(f"Failed: {f} : is absent in {directory2}")
            continue
        df1 = pd.read_csv(files1[f])
        df2 = pd.read_csv(files2[f])
        if set(df1.columns) != set(df2.columns):
            print(f"Failed: {f} : number of columns do not match")

        index1, numeric_cols1 = get_index_cols(df1)
        index2, numeric_cols2 = get_index_cols(df2)

        if len(df1) != len(df2):
            print(f"Failed: {f} : Number of rows does not match")

        if set(numeric_cols1) != set(numeric_cols2):
            print(f"Failed: {f} : Number of numeric columns does not match")

        index = list(set(index1) & set(index2))

        df1_ = df1.groupby(index).sum(numeric_only=True)
        df2_ = df2.groupby(index).sum(numeric_only=True)

        for c in numeric_cols1:
            rerror = (df1_[c]-df2_[c])/df1_[c]
            r = np.abs(rerror) > 1e-5
            if r.sum() != 0:
                print(f"Failed: {f} : Results do not match for {c}")
                # print(rerror[r])
                break
        else:
            # this else is at for loop level
            # get executed if there no break statement occures during
            # execution of entire loop.
            # if the loop breaks, then this else will not get executed
            print("OK: {f} : Results match".format(f=f))

            if len(df1) == len(df2):
                diff = df1[index1].compare(df2[index2])
                if not diff.empty:
                    print(diff)
                    print(f"Row order mismatch : {f}")


def summary(logdata, totalfiles):
    match = 0
    failed = 0
    absent = 0
    order = 0
    for line in logdata.split("\n"):
        if "Results" in line:
            if "OK:" in line:
                match += 1
            elif "Failed:" in line:
                failed += 1
                print(line)

        elif "Failed:" in line:
            if "absent" in line:
                absent += 1
            else:
                failed += 1
            print(line)
        elif "order" in line:
            order += 1
            print(line)
    print("="*30)
    print("Results match for       :", match)
    print("Results do not match for:", failed)
    print("Order mismatch for      :", order)
    print("Extra result files      :", absent)
    print("Total result files      :", totalfiles)
    print("="*30)


if __name__ == "__main__":
    new = sys.argv[1]
    orig = sys.argv[2]
    totalfiles = len(get_csvs(new))
    f = io.StringIO()
    with redirect_stdout(f):
        main(new, orig)
    s = f.getvalue()
    # print(s)
    summary(s, totalfiles)
