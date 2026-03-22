# pdf-to-epub

> **[Read in English](README.md)**

Uma skill para o Claude que converte documentos PDF em arquivos EPUB, otimizados para e-readers e apps de leitura mobile como Apple Books, Kindle e Kobo.

## O problema

PDFs têm layout fixo. Funcionam bem no desktop, mas ler um PDF de 30 páginas no celular significa ficar o tempo todo ampliando, dando zoom e rolando na horizontal. EPUB é o formato nativo dos e-readers: o texto se ajusta a qualquer tela, o usuário controla o tamanho da fonte e o espaçamento, e a navegação por capítulos funciona nativamente.

Essa skill ensina o Claude a pegar qualquer PDF e produzir um EPUB limpo e bem estruturado, confortável de ler no celular, tablet ou e-reader.

## O que faz

- Extrai conteúdo de PDFs enviados pelo usuário, preservando a estrutura original (capítulos, títulos, blocos de código, tabelas, listas)
- Gera arquivos EPUB 3 válidos com CSS embutido, sumário navegável e suporte UTF-8
- Traduz o conteúdo para qualquer idioma quando solicitado, mantendo trechos de código e termos técnicos intactos
- Produz arquivos compatíveis com Apple Books, Kindle (via Send to Kindle), Kobo e qualquer leitor compatível com EPUB

## Instalação

### Claude.ai

1. Baixe a [última release](../../releases/latest) (arquivo .zip)
1. Vá em **Settings > Capabilities > Skills**
1. Clique em **Upload skill** e selecione o arquivo .zip
1. Ative a skill

### Claude Code

```bash
git clone https://github.com/viniciusgomesai/pdf-to-epub.git ~/.claude/skills/pdf-to-epub
```

## Como usar

Envie um PDF para o Claude e peça a conversão:

- “Converte esse PDF pra EPUB pra eu ler no iPhone”
- “Transforma esse documento em ebook pro Apple Books”
- “Quero ler esse PDF no Kindle, converte pra mim”
- “Converte esse PDF pra EPUB e traduz pro inglês”

A skill é ativada automaticamente quando o Claude identifica que você quer converter um PDF para leitura mobile ou em e-reader.

## Como funciona

|Arquivo                 |Finalidade                                                                                                                                                             |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`SKILL.md`              |Instruções que ensinam ao Claude o fluxo completo de conversão: como extrair a estrutura do PDF, mapear para capítulos EPUB, lidar com tradução e gerar o arquivo final|
|`scripts/create_epub.py`|Script Python reutilizável que recebe uma definição de livro em JSON e gera um arquivo EPUB 3 válido com tipografia embutida e navegação                               |

O Claude lê o PDF, planeja a estrutura de capítulos, monta uma definição em JSON e passa para o script. O resultado é um arquivo EPUB pronto para leitura.

## Requisitos

- Python 3.8+
- `ebooklib` (instalado automaticamente pela skill quando necessário)

## Estrutura de arquivos

```
pdf-to-epub/
├── SKILL.md              # Instruções da skill (para o Claude)
├── scripts/
│   └── create_epub.py    # Script de geração do EPUB
├── README.md             # Versão em inglês
├── README.pt-BR.md       # Este arquivo
└── LICENSE
```

## Dicas

- **Apple Books**: Envie o EPUB via AirDrop para seu iPhone/iPad ou abra pelo app Arquivos. Ele abre direto no Livros.
- **Kindle**: Use o serviço [Send to Kindle](https://www.amazon.com/sendtokindle) da Amazon para enviar o EPUB ao seu dispositivo Kindle.
- **Tradução**: Ao pedir tradução, o Claude preserva trechos de código, comandos de terminal, caminhos de arquivo e identificadores técnicos no idioma original, já que precisam ser usados exatamente como escritos.

## Licença

MIT
