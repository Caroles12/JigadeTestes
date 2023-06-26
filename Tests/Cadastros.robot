*** Settings ***
Documentation

Resource    ./../Resources/componentesDigitais.robot

*** Test Cases ***

Caso de teste para adicionar esquematico de um componente
    [Documentation]    Caso de Testes para adicionar o esquemático de um componente
    Dado que o arquivo esteja no diretório    ./Cadastros/esquematicoDoComponente.txt    
    Quando o arquivo estiver preenchido com os dados do esquematico do componente
    Então adicione na base de dados


Caso de teste para adicionar os resultados esperados para um componente
    [Documentation]    Caso de Testes para adicionar os resultados esperados
    Dado que o arquivo esteja no diretório    ./Cadastros/resultadosEsperadosDoComponente.txt    
    Quando o arquivo estiver preenchido com os dados dos resultados do componente
    Então adicione na base de dados    
         


