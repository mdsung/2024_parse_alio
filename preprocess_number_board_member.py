from pathlib import Path

import pandas as pd


def process_dataframe(data: pd.DataFrame):
    data["col_name"] = data.apply(lambda x: f"{x['구분.2']} {x['구분.3']}", axis=1)
    procssed_data = pd.concat(
        [
            data.iloc[0:9, [-1, -2]],
            data.iloc[23:24, [3, 9]].rename(columns={"구분.3": "col_name"}),
        ]
    )
    columns = procssed_data["col_name"].tolist()
    values = procssed_data.iloc[:, 1].tolist()
    return columns, values


def main():
    output = {}
    for f in Path("data/raw/임직원수").glob("*.csv"):
        data = pd.read_csv(f)
        columns, values = process_dataframe(data)
        output[f.stem] = values
    df = pd.DataFrame(output, index=columns).T
    df.to_excel("data/processed/임직원수/임직원수.xlsx")


if __name__ == "__main__":
    main()
