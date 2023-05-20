*** Settings ***

Library    ./../Scripts/testedeComponentes.py
Library    ./../Scripts/database.py
Library    OperatingSystem 
Library    JSONLibrary
Library    BuiltIn

*** Variables ***
${NomedoComponente}
&{esquematico}
${deviceConnected}
@{results}
${endResult}
${arquivo_Componente} 


*** Keywords ***

Retorne o esquemático de ligação do componente com o DAQ
    [Arguments]    ${NomedoComponente}
    Set Global Variable    ${NomedoComponente}
    &{esquematico}=    Return Esquematico De Ligacao    ${NomedoComponente}
    Log To Console    ${esquematico}
    Set Global Variable    &{esquematico}
    

Dado que o DAQ esteja conectado a porta USB
    ${deviceConnected}=    Check Device Connected
    Should Be True    ${deviceConnected}  
    Log To Console    ${deviceConnected}  

Quando for realizado o teste do componente escolhido
    @{results}=    Make The Test For Component    ${esquematico}
    Set Global Variable     @{results}

Entao verifique que o componente esta funcionando 
    ${endResult}=    Check Results   ${results}
    Should Be True    ${endResult}
    IF  ${endResult}
        Log    Testes Funcionaram
    END

Dado que o arquivo esteja no diretório
    [Arguments]     ${arquivo_Componente}
    ${result}=   Run Keyword And Return Status    File Should Exist    ${arquivo_Componente}
    Set Global Variable    ${arquivo_Componente}
    Should Be True    ${result}

Quando o arquivo estiver preenchido com os dados do esquematico do componente        
    ${tamanhoDoArquivo}  Run  ls -l "${arquivo_Componente}" | awk '{print $5}'
    Should Not Be Equal As Strings  ${tamanhoDoArquivo}  0

Quando o arquivo estiver preenchido com os dados dos resultados do componente
    ${tamanhoDoArquivo}  Run  ls -l "${arquivo_Componente}" | awk '{print $5}'
    Should Not Be Equal As Strings  ${tamanhoDoArquivo}  0    

Então adicione na base de dados
    ${result}=    Add Document In The Collection    ${arquivo_Componente}
    Should Be True    ${result}    

