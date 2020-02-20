# Dashboard

Simple dash board to visualize research progress.

Right now the dashboard is table based.
Each row in a table is an entry in the dashboard.
The entry is parsed automatically, the fist integer / float value is plotted.
Any string preceding this entry is is used as a label.
Any preceding date is used as timestamp.

Special names are
 * 's:\w*=.*' specify table settings (see TableSettings)
   - `s:\w*` enables a boolean flag
 * 'i:' ignore this entry
 * 'b:' baseline visualized as a horizontal line
 
 
Every sheet of a table will be visualized in a tab. The tabs can be sorted using the `s:priority=??` tag where `10` is the default priority.
You can customize what is shown in the table by settings the number of top results `s:keep_top=??`, and the number of most recent results `s:keep_last=??`.
By default the top entries are the ones with the highest value, if you'd like to visualize the lowest use `s:lower_better`.
The y-axis label is specified as `s:axis=...`. To hide a sheet use `s:hide`.

Here is a simple example of a table

**Sheet 1 - COCO**

| s:axis=mAP |  | |
|---|---|---|
| b:some baseline | 1/2/2020 12:00:00 | 10.1 |
| b:other baseline | 1/2/2020 12:00:00 | 20.5 |
| first model | 1/3/2020 | 22.5 |
| second model | 1/4/2020 | 23.5 |
| tenth model | 1/10/2020 | 30.0 |

**Sheet 2 - KITTI**

| s:axis=error | s:lower_better | s:keep_top=10 |
|---|---|---|
| b:some baseline | 1/2/2020 12:00:00 | 20.5 |
| b:other baseline | 1/2/2020 12:00:00 | 15.5 |
| first model | 1/3/2020 | 17.7 |
| second model | 1/4/2020 | 13.2 |
| tenth model | 1/10/2020 | 0.001 |
