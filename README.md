# Gruppen - Contato

## Modo de usar

## Desenvolvimento

### Instalando Dependências

O projeto utiliza python 3.7.<br>
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

Em seguida, execute o arquivo `main.py` de dentro da pasta `interface`:<br>

```cli
cd ./interface
python main.py
```

## Gerando um executável
