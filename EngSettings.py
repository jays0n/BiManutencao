
###############################################################################################################################################################
#
# Modulo : Settings        Data de Criação: 22/03/2023
#
# Objetivo: Modulo configuração do arquivo config.json
#
# Ultimas alteracoes: Criacao
#
# Data da ultima alteracao: 14/12/2022
#
# Desenvolvedor: Francisco J. E. de Sousa
#
# Contato: e-mail: francisco.sousa1993@outlook.com      tel: (21) 96965-6759
#
###############################################################################################################################################################

# Imports:
import json

def Read_Config():
    path="config.json"
    file_open=open(path,)
    return json.load(file_open)

def Update_Config():
    data=Read_Config()
