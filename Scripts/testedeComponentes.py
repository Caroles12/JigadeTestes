import nidaqmx
import pprint
import pandas as pd
import time 
from esquematico import return_esquematico_de_ligacao
from database import return_expected_result,return_allLinesDaq_digitalVersion
from nidaqmx.constants import (LineGrouping)

#.\teste.bat

pp = pprint.PrettyPrinter(indent=4)

def make_the_test_for_component(esquematico):
    componentName = esquematico["nomeDocomponente"] 
    expected_results=return_expected_result(esquematico["nomeDocomponente"])
    pinosEntradaDaq = []
    pinosSaidaDaq = []
    for pinoDaq,pinoComponente in esquematico.items():
        if 'componente para entrada de sinal' in pinoComponente:
            componente = pinoDaq.split(':')
            for valorComponentes in componente:
                if 'Numero' in valorComponentes:
                    continue
                else:
                    pinosEntradaDaq.append(valorComponentes)
        elif 'componente para saida de sinal' in pinoComponente:
            componente = pinoDaq.split(':')
            for valorComponentes in componente:
                if 'Numero' in valorComponentes:
                    continue
                else:
                    pinosSaidaDaq.append(valorComponentes)
        else:
            continue    
    values = get_values_to_write(expected_results,componentName)       
    result = write_digital_ports(pinosEntradaDaq,values,componentName,expected_results,pinosSaidaDaq)   
    return result

def check_results(results):
    listResult = []
    for i in results:
        for j in i:
            for x in j:
                listResult.append(x)
    
    return len(set(listResult)) == 1 

def get_values_to_write(expected_results,componentName):
    df = pd.DataFrame(data=expected_results)

    totaldecolunas=0
    for numerodecolunas in df.columns:
        if'case' in numerodecolunas:
            totaldecolunas=totaldecolunas+1

    numerodelinhas = len(df.index)-1   

    valoresentrada1=[]
    
    for entrada1 in range(1,totaldecolunas+1):   
        valorentrada1 = df.at["entrada1",'case'+str(entrada1)]
        if valorentrada1 == 1:
            valoresentrada1.append(True)
        else:
            valoresentrada1.append(False)    
    
    if componentName != 'NOT':
        valoresentrada2=[]    
        for entrada2 in range(1,totaldecolunas+1):   
            valorentrada2 = df.at["entrada2",'case'+str(entrada2)]
            if valorentrada2 == 1:
                valoresentrada2.append(True)
            else:
                valoresentrada2.append(False)    
            keys_value = list(zip(valoresentrada1,valoresentrada2))
    else:
        keys_value = valorentrada1 
    return keys_value
    
def compare_the_values(expected_results,values):
    expected_results2 = []
   
    if expected_results == values:
        expected_results2.append(True)
    else:
        expected_results2.append(False)      
            
    return expected_results2
       
def get_DAQlines_to_write(record,portasUtilizadas):
    allLines = []
    ports=[0,0,0]
    for lines,linePinsNumber in record.items():
        if str(linePinsNumber) in portasUtilizadas:
            if 'p0' in lines:
                ports[0]=1
                allLines.append(lines[3])
    
    return ports,allLines                

def get_DAQlines_to_read(record, lines, portasUtilizadas):
    readLines = []
    ports = [0,0,0]
    for liness,valoresLines in record.items():
            portLine = liness
            if portLine != 'DGND':
                if str(valoresLines) in portasUtilizadas:
                    lineNaoUtilizados = portLine.replace('p','').split('_')
                    if lineNaoUtilizados[1] not in lines:
                        readLines.append(lineNaoUtilizados[1])
                        if 'p0' in portLine:
                            ports[0]=1
                        elif 'p1' in portLine:
                            ports[1]=1
                        elif 'p2' in portLine:
                            ports[2]=1
                        else:
                            continue    

    return readLines               

def mix_read_and_write_lines(writeDaqLines,readDaqLines,componentName):
    j=0
    final = {}
    if componentName == 'NOT':
        for i in range(0,len(readDaqLines)):
            item = readDaqLines[i]
            final[item] = writeDaqLines[i]
    else:    
        for i in range(0,len(readDaqLines)):
            item = readDaqLines[i]
            final[item] = [writeDaqLines[j],writeDaqLines[j+1]]  
            j+=2
    return final
    


def write_digital_ports(portasUtilizadas, values, componentName,expected_results,pinosSaidaUtilizados):
    record = return_allLinesDaq_digitalVersion()
    ports,allLines = get_DAQlines_to_write(record,portasUtilizadas)
    lines = []
    result = []
    for alllines in allLines:
        lines.append(alllines)     
    readLines = get_DAQlines_to_read(record,lines,pinosSaidaUtilizados) 
    lines = mix_read_and_write_lines(allLines,readLines,componentName)  
    
    if componentName != 'NOT':  
        for value1,value2 in values:    
            for i in range(0, len(readLines)):
                keyValue = readLines[i]
                with nidaqmx.Task() as task:
                    task.do_channels.add_do_chan(
                        "Dev1/port0/line" + lines[keyValue][0] + ":" + lines[keyValue][1], line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
                    )

                    try:
                        print("N Lines 1 Sample Boolean Write (Error Expected): ")
                        print(task.write([value1, value2],auto_start=True))
                    except nidaqmx.DaqError as e:
                        print(e)

                    with nidaqmx.Task() as task2:
                        task2.di_channels.add_di_chan("Dev1/port0/line8", line_grouping=LineGrouping.CHAN_PER_LINE)
                        data = task2.read()
                
                
              
                #with nidaqmx.Task() as task:
                #    try:
                #        print("é o 1'Dev1/port0/line" + lines[keyValue][0] +"valor escrito=",value1 )
                #        task.do_channels.add_do_chan(
                #        "Dev1/port0/line" + lines[keyValue][0],
                #        line_grouping=nidaqmx.constants.LineGrouping.CHAN_PER_LINE)
                #        task.write(True,auto_start=True)
                #        task.start()
                #    except nidaqmx.DaqError as e:
                #        print(e)
                #        print('\n')
                #with nidaqmx.Task() as task2:            
                #    try:
                #        print("é o 1'Dev1/port0/line" + lines[keyValue][1] +"valor escrito=",value2 )
                #        task2.do_channels.add_do_chan(
                #        "Dev1/port0/line" + lines[keyValue][1],
                #        line_grouping=nidaqmx.constants.LineGrouping.CHAN_PER_LINE)
                #        task2.write(True,auto_start=True)
                #        task2.start()
                    #    print("é o 2'Dev1/port0/line" + lines[keyValue][1] +"valor escrito=",value2)
                    #    task2.do_channels.add_do_chan(
                    #    "Dev1/port0/line" + lines[keyValue][1],
                    #    line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
                    #    task2.write(value2,auto_start=True)
                    #    task2.start()
                    #    print('lines',"Dev1/port0/line"+lines[keyValue][0]+ ":" +lines[keyValue][1])
                    #    task2.do_channels.add_do_chan("Dev1/port0/line"+lines[keyValue][0]+ ":" +lines[keyValue][1],line_grouping=nidaqmx.constants.LineGrouping.CHAN_PER_LINE)
                    #    #print('valores escritos',value1,value2)
                    #    print
                    #    task2.write([True,True],auto_start=True)
                    #    task2.start()
                        #results = read_digital_ports(keyValue,value1,value2,expected_results)
                        #result.append(results)
                #    except nidaqmx.DaqError as e:
                 #       print(e)

          
    

    return result

def get_the_expected_results_for_the_correct_case(value1,value2,expected_results):
    for i in expected_results:
        for j in i:
            if type(j) == dict:
                if j['entrada1'] == value1 and j['entrada2'] == value2:
                    expectedResultForThisCase = {'entrada1': value1, 'entrada2': value2, 'saida':j['saida']}

    return expectedResultForThisCase 
    
def read_digital_ports(line,value1,value2,expected_results):
    allresults = []
    expectedResultForThisCase = get_the_expected_results_for_the_correct_case(value1,value2,expected_results.items())
    with nidaqmx.Task() as task:
        task.di_channels.add_di_chan("Dev1/port0/line" + line,
                                    line_grouping=LineGrouping.CHAN_PER_LINE)
        data = task.read()
        time.sleep(10)
        values = {'entrada1': value1, 'entrada2': value2, 'saida':data}
        allresults2 = compare_the_values(expectedResultForThisCase,values)
        allresults.append(allresults2)   
    return allresults

def check_device_connected():
  local = nidaqmx.system.System.local()
  for device in local.devices:
    print('entrouuu')
    print('device',device)
    print(f'Device Name: {device.name}, Product Type: {device.product_type}')
    print('Input channels:', [chan.name for chan in device.ai_physical_chans])
    print('Output channels:', [chan.name for chan in device.ao_physical_chans])
    return True
  return False

if __name__ == '__main__':
    esquematico=return_esquematico_de_ligacao("74HC32")
    #print('todo o esquematico',esquematico) 
    #device_connected = check_device_connected()
    #make_the_component_power_supply(esquematico)
    #results = make_the_test_for_component(esquematico)
    #endResult = check_results(results)
    #print('valor de end',endResult)


