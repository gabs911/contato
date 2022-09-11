# Gruppen - Contato

## Modo de usar

## Desenvolvimento

### Instalando Dependências

É necessário python 3.7 ou posterior para executar o programa.<br>
Para instalar as dependências do projeto, garanta que a versão do pip seja 22.0.4 ou posterior e rode o arquivo [install_dependencies.sh](install_dependencies.sh) no terminal.

### Executando a Aplicação

Para executar a aplicação, adicione as configurações necessárias ao arquivo [config.json](interface/config.json),
o arquivo tem o seguinte formato:

```json
{
  "ambiente_eletronico": "teste",
  "ambiente_midi": "teste",
  "serial_port": "COM4",
  "midi_port": 1
}
```

`ambiente_eletronico` e `ambiente_midi` aceitam os valores `"teste"` ou `"producao"`.  
Caso deseje apenas simular o comportamento para determinada comunicação, escolha `"teste"` e vão ser criados Mocks para os mesmos. Se deseja executar a aplicação com o dispositivo eletrônico e/ou a porta MIDI, o valor deve ser `"producao"`.

Em seguida, navegue para a pasta `interface` e execute o arquivo [main.py](interface/main.py) :<br>

```cli
cd ./interface
python main.py
```

## Gerando um executável

### Instalando o gerador de executável

É possível gerar um executável usando auto-py-to-exe, para instalar use o comando

```cli
pip install auto-py-to-exe
```

Para executar auto-py-to-exe após a intalação,apenas navegue para a pasta `interface` execute o comando `auto-py-to-exe`:

```cli
cd ./interface
auto-py-to-exe
```

Será aberto uma interface onde é possível configurar as opções para a build.

### Usando o auto-py-to-exe

Em cada campo, siga as instruções

- Script location: Escolha o arquivo [main.py](interface/main.py) na pasta [interface](interface).
- OneFile: Escolha `OneDirectory` (a opção `OneFile` é problemática com arquivos de imagens e .json, o formato como são guardadas as informações).
- Icon: Escolha a logo do Gruppen (Deve ser um arquivo .ico 64x64).
- Additional Files:
  - adicione o arquivo [config.json](interface/config.json) clicando em `Add Files`, deixe o padrão `.` como local para enviar o arquivo
  - adicione a pasta [resources](interface/resources) clicando em `Add Folders`, como local para enviar escolha `resources/`.

Por fim gere um executável clicando no botão `Convert .py to .exe` e uma pasta output será gerada, dentro de `main` terá o executável `main.exe`.
