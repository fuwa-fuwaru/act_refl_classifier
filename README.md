# Active-reflexive classifier

A program for analysing interview transcripts and determining respondent's prevalent metaprogram on the active-reflexive
  spectrum.

## Input format

.tsv or .txt (respondent prefix: "PAR: ")

## Use cases

### Get interview statistics for files and/or directories

```python3 act_refl_classifier.py interview_1.txt```

```python3 act_refl_classifier.py interviews```

### Compare to existing annotation

```python3 act_refl_classifier.py interview_2.tsv -c```

### Export statistics summary for several files

```python3 act_refl_classifier.py interviews interview_4.txt --output summary.tsv```

### Export table with new (and old, if present) annotation

```python3 act_refl_classifier.py interview_5.tsv --no-display -e interview_3_new.tsv```