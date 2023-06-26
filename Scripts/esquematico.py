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
            if pinosDAQ in pinosUtilizadosDAQ:
                pinosUtilizadosDAQ.remove(pinosDAQ) 
                keysDaqUtilizadas.append(keysDAQ[ind])
                    
        for pinosDaq,pinosDoComponenteSaida in zip(pinosUtilizadosDAQ,saidasDoComponente):
            if pinosDaq in pinosDigitaisDaqKeys.values():
                ind = keysDAQValues.index(pinosDaq)
                esquematico["Numero do pino do DAQ(" + str(keysDAQ[ind]) + ")" +":" + str(pinosDaq)] = "Numero do pino do componente para saida de sinal:" + str(pinosDoComponenteSaida)
                pinosUtilizadosDAQ.remove(pinosDaq)
                keysDaqUtilizadas.append(keysDAQ[ind]) 
                    
        
        esquematico["Numero do pino do DAQ para alimentacao(+5V):" + str(pinoAlimentacaoDAQ) + " ou " + str(pinoAlimentacaoDAQ2)] = "Numero do pino do componente para alimentacao de" + str(valorAlimentacaoDoComponente)  + "V:" + str(pinoAlimentacao)    
        esquematico["Numero do pino GND do DAQ(DGND):" + str(daq_pins["pinosDigitais"]["DGND"])] = "Numero do pino do componente para de GND" + str(pinoGND) + ":" + str(valorGNDDoComponente)

        pinosDigitaisGND=daq_pins["pinosDigitais"]["DGND"]
        removeKeys=set(keysDaqUtilizadas)&set(keysDAQ)

        for remove in removeKeys:    
            keysDAQ.remove(remove)

        salvar_esquematico(esquematico)
        return esquematico

