import nidaqmx
from nidaqmx.constants import (LineGrouping)
from nidaqmx.constants import WAIT_INFINITELY

lineEntrada1 = '0'
lineEntrada2 = '1'
linedeLeitura = '10'; #trocar pro line certo
sampleRate = 50000
value1=True
value2=True

for i in range(0,45):
    with nidaqmx.Task() as read_task, nidaqmx.Task() as write_task:
                with nidaqmx.Task() as read_task, nidaqmx.Task() as write_task:
                    write_task.do_channels.add_do_chan(
                        "Dev1/port0/line" + lineEntrada1 + ":" + lineEntrada2, line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
                    read_task.di_channels.add_di_chan("Dev1/port0/line" + linedeLeitura,
                                    line_grouping=LineGrouping.CHAN_PER_LINE)
                    print('line de escrita',lineEntrada1,lineEntrada2)

                    for task in (read_task, write_task):
                        task.timing.cfg_samp_clk_timing(rate=sampleRate, source='OnboardClock', samps_per_chan=1)

                    write_task.triggers.start_trigger.cfg_dig_edge_start_trig(
                                                    read_task.triggers.start_trigger.term)
                    
                    write_task.write([value1, value2], auto_start=False)

                    write_task.start()  

    
                    indata = read_task.read(1, timeout=WAIT_INFINITELY)

                    print("valor de read",indata)