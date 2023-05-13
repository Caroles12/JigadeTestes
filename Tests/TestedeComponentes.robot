*** Settings ***
Documentation

Resource    ./../Resources/componentesDigitais.robot

Test Setup    Obtendo o esquematico de ligacao entre o DAQ e o componente a ser testado

*** Variables ***
${componenteEscolhido}=    74HC08

*** Keywords ***

Obtendo o esquematico de ligacao entre o DAQ e o componente a ser testado
    Retorne o esquemático de ligação do componente com o DAQ    ${componenteEscolhido} 
    Sleep    2s
 

*** Test Cases ***

Caso de teste para componentes eletronicos
    [Documentation]    Caso de Testes de CI's escolhidos pelo usuário
    Dado que o DAQ esteja conectado a porta USB
    Quando for realizado o teste do componente escolhido 
    Entao verifique que o componente esta funcionando
         


