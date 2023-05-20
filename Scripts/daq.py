"""Example for writing digital signal."""
import nidaqmx
from nidaqmx.constants import LineGrouping


with nidaqmx.Task() as task:
    task.do_channels.add_do_chan(
        "Dev1/port0/line2:3", line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
    )

    try:
        print("N Lines 1 Sample Boolean Write (Error Expected): ")
        print(task.write([True, True],auto_start=True))
    except nidaqmx.DaqError as e:
        print(e)

with nidaqmx.Task() as task2:
    task2.di_channels.add_di_chan("Dev1/port0/line10", line_grouping=LineGrouping.CHAN_PER_LINE)
    data = task2.read()
    print(data)