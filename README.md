# Gruppen - Contato

## Modo de usar

## Desenvolvimento

### Instalando Dependências

É necessário que a versão do python seja >= 3.7 e <= 3.10 para executar o programa.<br>
Para instalar as dependências do projeto, garanta que a versão do pip seja 22.0.4 ou posterior e rode o arquivo [install_dependencies.sh](install_dependencies.sh) no terminal.

### Executando a Aplicação

Para executar a aplicação, adicione as configurações necessárias ao arquivo [config.json](interface/config.json),
o arquivo tem o seguinte formato:

```json
{
  "ambiente_eletronico": "teste",
  "ambiente_midi": "producao",
  "ambiente_file_service": "dev",
  "app_name": "Contato"
}
```

`ambiente_eletronico` e `ambiente_midi` aceitam os valores `"teste"` ou `"producao"`.  
O valor `"teste"` significa que aquele componente vai ser executado como um Mock que simula o comportamento real.  
O valor `"producao"` significa que aquele modulo vai executar utilizando a aquele componente.  
Para `ambiente_file_service` os valores possíveis são `"producao"` e `"dev"`. `"producao"` significa que o módulo de arquivos buscará os presets dentro de `LOCALAPPDATA` enquanto `"teste"` significa que buscará dentro da estrutura de arquivos do projeto. É recomendado usar `"dev"` para qualquer desenvolvimento e `"producao"` para quando for gerar um executável e instalador.  
Em seguida, navegue para a pasta `interface` e execute o arquivo [main.py](interface/main.py) :<br>

```shell
cd ./interface
python main.py
```

## Gerando um executável

### Instalando o gerador de executável

É possível gerar um executável usando auto-py-to-exe, para instalar use o comando

```shell
pip install auto-py-to-exe
```

Para executar auto-py-to-exe após a intalação,apenas navegue para a pasta `interface` execute o comando `auto-py-to-exe`:

```shell
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

## Gerando o instalador

Está sendo usado o gerador de instalador chamado [Install Forge](https://installforge.net/), ele pode ser baixado e instalado [aqui](https://installforge.net/download/).

### Tutorial Básico de Install Forge

Um tutorial de como usar `Install Forge` em conjunto com `pyinstaller` pode ser encontrado [aqui](https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/).  
(A ferramenta auto-py-to-exe usa pyinstaller por baixo dos panos, então o tutorial é válido e pode só pular a parte que lida com `pyinstaller`).

### Descobrindo a versão atual

Para gerar um instalador você deve informar uma versão. O valor da última versão pode ser encontrada rodando o arquivo [achar-git-tag.sh](achar-git-tag.sh) no terminal.

```shell
./achar_git_tag.sh
```

o resultado será um valor no seguinte formato: `v<major>.<minor>.<hotfix>`.  
Exemplo:

```cli
v1.0.0
```

### Determinando nova versão

- Alterações pequenas ou correções de bugs devem aumentar o valor da versão `<hotfix>` em 1.
  - Exemplo:  
    _A versão atual é v2.3.9 e é consertado um bug na calibração, a próxima versão a ser gerada é a v2.3.10_.
- Implementações de mudanças de regra de negócio devem aumentar o valor da versão `<minor>` em 1.
- Alterações drásticas, migração para outras tecnologias e mudanças que causem falta de compatibilidade com versões anteriores devem aumentar o valor da versão `<major>` em 1.

### Gerando uma nova versão

Tendo determinado a versão nova, crie uma tag nova no commit que gera a nova versão com o commando **git tag**.  
Exemplo:

```shell
git tag v2.3.9
```

No `Install Forge`, na área dedicada a versão, adicione a nova versão que foi determinada.
