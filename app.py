###############################################################################################################################################################
#
# Módulo : ENG Main          Data de Criação: 17/10/2022
#
# Objetivo: Módulo Principal da aplicação
#
# Ultimas alterações: Criação
#
# Data da ultima alteração: 17/10/2022
#
# Desenvolvedor: Francisco J. E. de Sousa
#
# Contato: e-mail: francisco.sousa1993@outlook.com      tel: (21) 96965-6759
#
###############################################################################################################################################################

# Imports:

import EngClsGui as gui


gui_interface=gui.GraficInterface()

'''
ds_manutencao_atrasada=gui.Dash_Manutencao_Atrasada()
ds_aggman=gui.Dash_Aggman()
ds_disponibilidade=gui.Dash_Disponibilidade()

gui_interface.Add('manutencoesatrasadas','Manutenções Atrasadas',ds_manutencao_atrasada.Create())
gui_interface.Add('aggman','Indicador AGGMAN',ds_aggman.Create())
gui_interface.Add('disponibilidade','Disponibilidade',ds_disponibilidade.Create())

'''
gui_interface.Run()
