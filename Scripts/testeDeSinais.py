import time
import nidaqmx

with nidaqmx.Task() as task, nidaqmx.Task() as read_task:
    task.do_channels.add_do_chan("Dev1/port0/line0:1", line_grouping=nidaqmx.constants.LineGrouping.CHAN_PER_LINE)
    read_task.di_channels.add_di_chan("Dev1/port0/line8", line_grouping=nidaqmx.constants.LineGrouping.CHAN_PER_LINE)

    while(True):
        task.stop() 
        task.write([True, True], auto_start=True)
        time.sleep(2)
        data = read_task.read()
        task.write([False, True], auto_start=True)
        time.sleep(2)
        data = read_task.read()
        task.write([True, False], auto_start=True)
        time.sleep(2)
        data = read_task.read()
        task.write([False, False], auto_start=True)
        time.sleep(2)
        data = read_task.read()
        
