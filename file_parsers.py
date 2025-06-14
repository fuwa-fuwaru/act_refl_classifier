import click
import pandas as pd
import re


def print_res(meta, score, annot=False):
    pref = "Annotated" if annot else "Predicted"
    click.echo(pref + " metaprogram: " + meta + ". Prevalence score: " + f"{score:.0%}")


def get_res(column):
    pred_counter = column.value_counts()
    if pred_counter["active"] == pred_counter["reflexive"]:
        pred = "undefined"
        pred_score = 0.5
    elif pred_counter["active"] > pred_counter["reflexive"]:
        pred = "active"
        pred_score = pred_counter["active"] / (pred_counter["active"] + pred_counter["reflexive"])
    else:
        pred = "reflexive"
        pred_score = pred_counter["reflexive"] / (pred_counter["active"] + pred_counter["reflexive"])
    return pred, pred_score


def parse_data(data, comp, display):
    pred, pred_score = get_res(data['new-act-refl'])
    if display:
        print_res(pred, pred_score)
    annot = "-"
    annot_score = -1
    if display and comp:
        if 'active-reflexive' in data.columns:
            annot, annot_score = get_res(data['active-reflexive'])
            if display:
                print_res(annot, annot_score, annot=True)
        else:
            click.echo('Annotation not present. For comparison please make sure the file has a column with annotations '
                       'titled "active-reflexive".')
    return pred, pred_score, annot, annot_score


def parse_file(path, pipe):
    if path.endswith('.tsv'):
        return parse_tsv(path, pipe)
    elif path.endswith('.txt'):
        return parse_txt(path, pipe)
    else:
        return []


def parse_tsv(path, pipe):
    click.echo("Interview: " + path)
    data = pd.read_csv(path, sep='\t')
    quotes = data["respondent"].tolist()
    labels = ["active" if res["label"] == "LABEL_1" else "reflexive" for res in pipe(quotes)]
    data["new-act-refl"] = pd.Series(labels)
    return data


def parse_txt(path, pipe):
    click.echo("Interview: " + path)
    quotes = []
    with open(path, "r", encoding='utf-8') as script:
        for line in script:
            if line.startswith('PAR: '):
                quotes.extend(quote_split(line[5:]))
    data = pd.DataFrame(quotes, columns=['respondent'])
    labels = ["active" if res["label"] == "LABEL_1" else "reflexive" for res in pipe(quotes)]  # SWITCH??????????
    data["new-act-refl"] = pd.Series(labels)

    return data


def quote_split(quote, max_len=256):
    if len(quote) <= 256:
        return [quote.rstrip('\n')]
    start_idx = 0
    split_quotes = []
    for m in re.finditer(r'[.!?] |[.!?]$', quote.rstrip('\n ')):
        if max_len - len(quote[start_idx:m.end()]) - max_len <= 30 or len(quote[start_idx:m.end()]) >= max_len\
                or m.end() == len(quote):
            split_quotes.append(quote[start_idx:m.end()].rstrip('\n '))
            if quote[m.end():].startswith(' '):
                start_idx = m.end() + 1
            else:
                start_idx = m.end() + 0
    return split_quotes

