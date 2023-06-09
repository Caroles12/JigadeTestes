from nidaqmx.constants import LineGrouping
import nidaqmx
import time 

for i in range(0,40):
     with nidaqmx.Task() as task, nidaqmx.Task() as read_task:
                         task.do_channels.add_do_chan(
                         "Dev1/port0/line0:1", line_grouping=LineGrouping.CHAN_PER_LINE
                         )
                         
                         print(task.write([True, True],auto_start=True))
                         read_task.di_channels.add_di_chan("Dev1/port0/line8",
                                        line_grouping=LineGrouping.CHAN_PER_LINE)
                         time.sleep(10)
                         data = read_task.read()
                         print('dado lido',data)

