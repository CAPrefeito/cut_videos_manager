# cut_videos_manager
App to cut videos in order to create many short videos quickly.

Os <b>executáveis</b> estão nas seguintes pastas:
<br>WINDOWS --> dist_win
<br>LINUX --> dist_linux


Para a execução do projeto <b>localmente</b> basta instalar as seguintes dependências no venv local:
<br>pip install PySimpleGUI
<br>pip install moviepy

Para gerar o executável localmente siga o seguinte processo:
<br>1º --> pyinstaller --onefile -w main.py (será gerado as pastas build e dist e o arquivo main.spec)
<br>No projeto existe dois arquivos de backup do main.spec
<br>Abra o arquivo de backup (win ou linux) e altera o caminho da lib do moviepy para o seu diretorio local (linhas 22 e 23)
<br>Após a atualização dos diretórios no arquivo main.spec, executar o seguinte comando
<br>2º --> pyinstaller main.spec