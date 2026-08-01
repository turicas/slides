import csv
import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def plot_from_csv_simple(csv_path: Path, output_image_path: Path, is_percentage: bool = False):
    """
    Cria um gráfico a partir de um arquivo CSV

    Assume que a primeira coluna é a data (eixo X) e todas as outras são séries de dados para o eixo Y.

    Args:
        csv_path (Path): Caminho para o arquivo CSV.
        output_image_path (Path): Caminho para o arquivo PNG
        is_percentage (bool): Se True, formata o eixo Y como percentual.
    """
    data = {}

    with csv_path.open() as infile:
        reader = csv.reader(infile)
        header = next(reader)
        for column_name in header:
            data[column_name] = []
        for row in reader:
            date_obj = datetime.datetime.strptime(row[0], "%Y-%m-%d")
            data[header[0]].append(date_obj)
            for i, value in enumerate(row[1:], start=1):
                numeric_value = float(value)
                data[header[i]].append(numeric_value)

    plt.style.use("seaborn-v0_8-darkgrid")
    fig, ax = plt.subplots(figsize=(14, 8))
    x_column_name = header[0]
    y_column_names = header[1:]
    x_values = data[x_column_name]
    for y_column in y_column_names:
        ax.plot(x_values, data[y_column], label=y_column)

    if is_percentage:
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=1))
        y_label = "(%)"
    else:
        y_label = "Valor"

    fig.autofmt_xdate()  # Rotaciona e alinha as datas no eixo X
    ax.set_xlabel("Data")
    ax.set_ylabel(y_label)
    title = csv_path.name.split("/")[-1].split("\\")[-1].replace(".csv", "").replace("_", " ").title()
    ax.set_title(f"Análise de: {title}")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(output_image_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--percent", action="store_true")
    parser.add_argument("csv_filename", type=Path)
    parser.add_argument("png_filename", type=Path)
    args = parser.parse_args()

    plot_from_csv_simple(args.csv_filename, args.png_filename, is_percentage=args.percent)
