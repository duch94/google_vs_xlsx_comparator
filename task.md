# Compare and update task

You given Google sheet and Excel file. 

You need:

1. Get Google Sheet contents
1. Load Excel file
1. Find difference between Sheet and Excel file.
   1. If difference found print it to user.    
   1. If difference found - ask user permission for update.
1. Write unit tests.
1. Create setup.py and any other required files for application distibution.
1. Keep code on github in public space


## Google Sheet structure

- Tab "Description" contains 3 rows with text "line 1" and "line 2 " and "line 3
  "

- Tab "Main" contains:

| ID   | Source component | Label           | Version | Type   | Description     |
| ---- | ---------------- | --------------- | ------- | ------ | --------------- |
| A1   | CMP1             | CMD_HH_AA_SIG_A | 1       | Metric | Sample metric A |
| A2   | CMP1             | CMD_HH_AA_SIG_B | 1       | Metric | Sample metric B |
| A3   | CMP2             | HH_BB_SIG       | 1       | Metric | Sample metric C |

- Tab "Extra" contains:

| ID   | Source component | Message name | Signal in message | Label           |
| ---- | ---------------- | ------------ | ----------------- | --------------- |
| A1   | CMP1             | MSG1         | CMDHHAASIGA       | CMD_HH_AA_SIG_A |
| A2   | CMP1             | MSG1         | CMDHHAASIGB       | CMD_HH_AA_SIG_B |
| A3   | CMP2             | MSG2         | HHBBSIG           | HH_BB_SIG       |

## XLSX structure

- Tab "Description" contains 3 rows with text "line 1" and "line 2" and "line 3"

- Tab "Main" contains:

| ID   | Source component | Label           | Version | Type   | Description     |
| ---- | ---------------- | --------------- | ------- | ------ | --------------- |
| A1   | CMP1             | CMD_HH_AA_SIG_A | 1       | Metric | Sample metric A |
| A2   | CMP1             | CMD_HH_AA_SIG_B | 1       | Metric | Sample metric B |
| A3   | CMP2             | HH_BB_SIG       | 2       | Metric | Sample metric C |
| A4   | CMP2             | HH_KK_SIG       | 1       | Metric | Sample metric D |

- Tab "Extra" contains:

| ID   | Source component | Message name | Signal in message | Label           |
| ---- | ---------------- | ------------ | ----------------- | --------------- |
| A1   | CMP1             | MSG1         | CMDHHAASIGA       | CMD_HH_AA_SIG_A |
| A2   | CMP1             | MSG1         | CMDHHAASIGB       | CMD_HH_AA_SIG_B |
| A3   | CMP2             | MSG2         | HHBBSIG           | HH_CC_SIG       |
| A4   | CMP2             | MSG3         | HHKKSIG           | HH_KK_SIG       |