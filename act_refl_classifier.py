import click
from pathlib import Path
import pandas as pd
import os
from file_parsers import parse_file, parse_data
from transformers import pipeline


@click.command(help="Determines respondent's prevalent metaprogram on the active-reflexive spectrum.")
@click.argument("paths",
                nargs=-1,
                type=click.Path(
                        exists=True,
                        file_okay=True,
                        dir_okay=True,
                        readable=True,
                        path_type=Path,
                    ),
                )
@click.option("-c",
              "--comp",
              is_flag=True,
              help="Compare to existing result (if input .tsv is annotated).",
              )
@click.option("--display/--no-display",
              ' /-N',
              help="Whether to display results in terminal (default=True).",
              default=True,
              )
@click.option("-o",
              "--output",
              nargs=1,
              type=click.Path(
                  file_okay=True,
                  dir_okay=False,
                  readable=True,
                  path_type=Path,
              ),
              help="Path to output .tsv file for result summary.")
@click.option("-e",
              "--export",
              nargs=1,
              type=click.Path(
                  file_okay=True,
                  dir_okay=False,
                  readable=True,
                  path_type=Path,
              ),
              help="Path to output .tsv file with machine (and human, if present in input) annotation.")


def cli(paths, comp, display, output, export):
    pipe = pipeline("text-classification", model="weights/checkpoint-100")
    click.echo("")
    if output:
        out_data = {"filename": [], "pred": [], "pred_score": [], "annot": [], "annot_score": []}
    for path in paths:
        if os.path.isdir(path):
            click.echo("Directory: " + path.name)
            for entry in path.iterdir():
                data = parse_file(path.name + '/' + entry.name, pipe)
                if type(data) is list:
                    continue
                pred, pred_score, annot, annot_score = parse_data(data, comp, display)
                if output:
                    out_data["filename"].append(path.name + '/' + entry.name)  # ??????
                    out_data["pred"].append(pred)
                    out_data["pred_score"].append(pred_score)
                    out_data["annot"].append(annot)
                    out_data["annot_score"].append(annot_score)
                if export:
                    data.to_csv(export, sep="\t")
                click.echo("")
        else:
            data = parse_file(str(path), pipe)
            if type(data) is list:
                continue
            pred, pred_score, annot, annot_score = parse_data(data, comp, display)
            if output:
                out_data["filename"].append(str(path))
                out_data["pred"].append(pred)
                out_data["pred_score"].append(f"{pred_score:.4f}")
                out_data["annot"].append(annot)
                out_data["annot_score"].append(f"{annot_score:.4f}")
            if export:
                data.to_csv(export, sep="\t")
            click.echo("")
    if output:
        pd.DataFrame.from_dict(out_data).to_csv(output, sep="\t")

if __name__ == "__main__":
    cli()
