#comando do rf metrics para gerar report
#robotmetrics --inputpath ./Results/ --output output.xml


from database import return_DAQ_schematic,return_component
import json
import numpy as np

def salvar_esquematico(esquematico):
    with open("esquematico.txt","w") as file:
        file.write(json.dumps(esquematico, indent=4))
        return "Esquematico salvo no arquivo"

def return_esquematico_de_ligacao(componente1):
    componente = return_component(componente1)
    daq_pins = return_DAQ_schematic()
    tipoDoComponente = componente["tipoDeComponente"]
    print('componente values',tipoDoComponente.values())
    print('olha o type ai', type(tipoDoComponente))
    if  len(tipoDoComponente) > 0:
        componenteEsperado = list(tipoDoComponente.values())[0]
        nomedoComponente = componente["nome"]
        entradasDoComponente = componente["entradas"]
        pinosDasEntradas = entradasDoComponente.values()
        saidasDoComponente = componente["saidas"].values()
        valorAlimentacaoDoComponente = componente["alimentacao"]["vcc"]
        valorGNDDoComponente = componente["referencia"]["pinoGND"]
        pinoAlimentacao = componente["alimentacao"]["pinoAlimentacao"]
        pinoGND = componente["referencia"]["gnd"]
        pinosDigitaisDaqAll = daq_pins["pinosDigitais"].values()
        #pinosAnalogicosDAQ = daq_pins["pinosanalogicos"].values()
        pinoAlimentacaoDAQ = daq_pins["alimentacao"]["+5Vpino1"]
        pinoAlimentacaoDAQ2 = daq_pins["alimentacao"]["+5Vpino2"]
        esquematico = {}
        esquematico["nomeDocomponente"] = nomedoComponente
        esquematico["tipoDeComponente"] = componenteEsperado
        pinosUtilizadosDAQ = list(pinosDigitaisDaqAll)
        pinosDigitaisDaqGND = []
        pinosDigitaisDaq = []
        pinosDigitaisDaqKeys = {}
        for keys in daq_pins["pinosDigitais"].keys():
            if 'GND' in keys:
                pinosDigitaisDaqGND.append(daq_pins["pinosDigitais"][keys])
                pinosUtilizadosDAQ.remove(daq_pins["pinosDigitais"][keys])
            else:
                pinosDigitaisDaqKeys[keys] = daq_pins["pinosDigitais"][keys]
                pinosDigitaisDaq.append(daq_pins["pinosDigitais"][keys])    
        keysDAQ = list(pinosDigitaisDaqKeys.keys())
        keysDAQValues = list(pinosDigitaisDaqKeys.values())
  
        
        keysDaqUtilizadas =[]
        for pinosDAQ,pinosDoComponenteEntrada in zip(pinosDigitaisDaq,pinosDasEntradas):
            if pinosDAQ in pinosDigitaisDaqKeys.values():
                ind = keysDAQValues.index(pinosDAQ)
                esquematico["Numero do pino do DAQ(" +str(keysDAQ[ind]) + ")" +":" + str(pinosDAQ)] = "Numero do pino do componente para entrada de sinal:" + str(pinosDoComponenteEntrada)
                #print('keyss daq in',keysDAQ[ind])
            if pinosDAQ in pinosUtilizadosDAQ:
                #print('valor de pinosDaq',pinosDAQ)
                #print('sao utilozados',pinosUtilizadosDAQ)
                pinosUtilizadosDAQ.remove(pinosDAQ) 
                keysDaqUtilizadas.append(keysDAQ[ind])
                    
        for pinosDaq,pinosDoComponenteSaida in zip(pinosUtilizadosDAQ,saidasDoComponente):
            if pinosDaq in pinosDigitaisDaqKeys.values():
                ind = keysDAQValues.index(pinosDaq)
                esquematico["Numero do pino do DAQ(" + str(keysDAQ[ind]) + ")" +":" + str(pinosDaq)] = "Numero do pino do componente para saida de sinal:" + str(pinosDoComponenteSaida)
                pinosUtilizadosDAQ.remove(pinosDaq)
                keysDaqUtilizadas.append(keysDAQ[ind]) 
                    
        #pinosAnalogicos = list(pinosAnalogicosDAQ)
        esquematico["Numero do pino do DAQ para alimentacao(+5V):" + str(pinoAlimentacaoDAQ) + " ou " + str(pinoAlimentacaoDAQ2)] = "Numero do pino do componente para alimentacao de" + str(valorAlimentacaoDoComponente)  + "V:" + str(pinoAlimentacao)    
        esquematico["Numero do pino GND do DAQ(DGND):" + str(daq_pins["pinosDigitais"]["DGND"])] = "Numero do pino do componente para de GND" + str(pinoGND) + ":" + str(valorGNDDoComponente)
        #for pinosDigitaisGND in pinosDigitaisDaqGND:

        #    esquematico["Numero do pino do digital GND do DAQ(DGND):" + str(pinosDigitaisGND)] = "Numero do pino do componente para de GND" + str(pinoGND) + ": " + str(valorGNDDoComponente)
        #print('leysDq',keysDaqUtilizadas)
        #print('vem q vem',keysDAQ)
        pinosDigitaisGND=daq_pins["pinosDigitais"]["DGND"]
        removeKeys=set(keysDaqUtilizadas)&set(keysDAQ)
        #print('all removekeys',removeKeys)
        #print('oq temos em',keysDaqUtilizadas)
        for remove in removeKeys:
            #print('todo o remove',remove)
            keysDAQ.remove(remove)
        #print('keyeyeyey',keysDAQ)
        #if len(cp2) != 0:
        #        esquematico = cria_esquematico_para_o_segundo_componente(cp2,pinosUtilizadosDAQ,esquematico,pinosDigitaisGND,pinoAlimentacaoDAQ,keysDAQ)
        salvar_esquematico(esquematico)
        print('tem o esquematico',esquematico)
        print('tipo do esquematico',type(esquematico))
        return esquematico

#duvida renan: como fazer essa questao do GDB
def cria_esquematico_para_o_segundo_componente(componente,pinosDisponiveis,esquematico,pinosDigitaisGND,pinoAlimentacaoDAQ,keysDaqUtilizadas):
    #print('keys daq22',keysDaqUtilizadas)
    #print('valor de pinos Utilizados',pinosDisponiveis)
    tipoDoComponente = componente["tipoDeComponente"]
    componenteEsperado = tipoDoComponente["portaLogica"]
    nomedoComponente = componente["nome"]
    entradasDoComponente = componente["entradas"]
    pinosDasEntradas = entradasDoComponente.values()
    saidasDoComponente = componente["saidas"].values()
    valorAlimentacaoDoComponente = componente["alimentacao"]["vcc"]
    valorGNDDoComponente = componente["alimentacao"]["pinoGND"]
    pinoAlimentacao = componente["alimentacao"]["pinoAlimentacao"]
    pinoGND = componente["alimentacao"]["gnd"]

    esquematico['Segundo Componete'] =  nomedoComponente
    esquematico['Tipo do Componete'] =  componenteEsperado
    #print('nome do componente',nomedoComponente)
    #print('valor de pin entradas',pinosDasEntradas)
    #print('valor de pinos da saida',saidasDoComponente)

    dicionario = dict(zip(keysDaqUtilizadas,pinosDisponiveis))
    #print('dictt',dicionario)

    for entradaComponente,pinosDAQ in zip(pinosDasEntradas,pinosDisponiveis):
        if pinosDAQ in dicionario.values():
                ind = pinosDisponiveis.index(pinosDAQ)
                #print('keyyy2',keysDaqUtilizadas[ind])
                if keysDaqUtilizadas[ind] == 'DGND':
                    continue
                else:    
                    esquematico["Numero do pino do DAQ(" + str(keysDaqUtilizadas[ind]) + ":" + str(pinosDAQ)] = "Numero do pino do componente para entrada de sinal:" + str(entradaComponente)
                pinosDisponiveis.remove(pinosDAQ)
 
    for saidaDoComponente,pinosDAQ in zip(saidasDoComponente,pinosDisponiveis):
        esquematico["Numero do pino do DAQ(" +":" + str(pinosDAQ)] = "Numero do pino do componente para saida de sinal:" + str(saidaDoComponente)
        pinosDisponiveis.remove(pinosDAQ)

    esquematico["Numero do pino do digital GND do DAQ(DGND):" + str(pinoGND)] = "Numero do pino do componente para de GND" + str(pinoGND) + ": " + str(valorGNDDoComponente)    

    return esquematico        