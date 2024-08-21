# Gerador de DANFes com Dados Aleatórios

Este projeto em Python 3.10 gera imagens de DANFes (Documento Auxiliar da Nota Fiscal Eletrônica) preenchidas com dados aleatórios. Ele utiliza bibliotecas como `xml.etree.ElementTree`, `PIL`, e `Faker` para criar e personalizar imagens de DANFes com informações simuladas.

## <span style="color: #DE3163;">Aviso Importante</span>

<span style="color: #DE3163;">
**Este projeto tem o objetivo exclusivo de ser utilizado em contextos de desenvolvimento tecnológico, como projetos de visão computacional e inteligência artificial, fornecendo dados fictícios para fins de teste e desenvolvimento. Não é destinado a qualquer uso ilegal ou para gerar documentos fiscais verdadeiros ou válidos.**

**Eu, como desenvolvedor deste projeto, repudio qualquer uso criminoso ou indevido desta ferramenta. Este projeto foi criado com a intenção de apoiar outros desenvolvedores em suas jornadas tecnológicas, dentro dos limites da lei. O uso para finalidades ilícitas vai contra os princípios deste trabalho, e não apoio, nem me responsabilizo por tal uso.**
</span>

## Bibliotecas Utilizadas

- `xml.etree.ElementTree`: Para manipulação de arquivos XML.
- `PIL`: Para criação e edição de imagens.
- `Faker`: Para geração de dados fictícios, como nomes, endereços e CPFs.
- `os`: Para manipulação de diretórios e arquivos.
- `random`: Para geração de números aleatórios.
- `textwrap`: Para ajustar textos dentro dos limites dos campos.

## Funcionalidades

- Gera imagens de DANFes baseadas em um modelo (`.png`) e preenche os campos com dados aleatórios.
- Ajusta automaticamente o tamanho das fontes e a quebra de linha para garantir que os dados fiquem dentro dos limites dos campos na imagem.
- Gera rótulos (labels) para cada imagem no formato adequado para sistemas de anotação de imagens, como YOLO.
- Configurável para gerar múltiplas imagens de uma só vez.

## Estrutura do Projeto
```
.
├── danfe_model.png # Imagem modelo da DANFe
├── paths.xml # Arquivo XML com a definição dos campos
├── LiberationSans-Regular.ttf # Fonte usada nas imagens geradas
├── output_images/ # Diretório de saída das imagens geradas
├── output_labels/ # Diretório de saída dos rótulos gerados
├── main.py # Código principal do projeto
└── README.md # Este arquivo
```

## Como Usar

### Pré-requisitos

Certifique-se de que as seguintes bibliotecas estão instaladas:

```bash
pip install Pillow faker textwrap3
````
### Configuração
Modifique as variáveis no início do arquivo main.py conforme necessário:

input_xml_path: Caminho para o arquivo XML com os campos da DANFe. (Já disponibilizo incluído um xml com tamanhos do modelo DANFe que estou utilizando.) 
input_image_path: Caminho para a imagem modelo da DANFe.
output_image_dir: Diretório onde as imagens geradas serão salvas.
output_labels_dir: Diretório onde os rótulos gerados serão salvos.
font_path: Caminho para o arquivo .ttf da fonte usada nas imagens.
num_images: Quantidade de imagens que deseja gerar.
Executando o Script
Basta rodar o script para gerar as DANFes:
````
python main.py
````
