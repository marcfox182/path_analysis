# Mapear as Rotas de Usuário para URLs com Análise de Links Internos (SEO com Python)

Este script Python ajuda a entender como os usuários navegam em seu site e os caminhos que eles seguem até alcançar páginas prioritárias. Combina dados do Screaming Frog e do Google Search Console para revelar a eficácia da arquitetura de informação do seu site e identificar áreas potenciais para melhoria.

É uma ferramenta essencial para [especialistas em SEO](https://www.marcostadeu.com.br/) que buscam aprimorar a arquitetura de informação de sites. Ao combinar dados de ferramentas como o Screaming Frog e o Google Search Console, este script Python oferece uma visão detalhada sobre como os usuários realmente navegam pelo site, quais rotas eles tomam e quais páginas atraem mais tráfego.

Para profissionais de SEO, entender esses caminhos é crucial para otimizar a experiência do usuário e melhorar os rankings de busca. O script permite identificar gargalos na navegação e avaliar a eficiência de textos de âncora e links internos. Com isso, é possível fazer ajustes estratégicos para garantir que as páginas mais importantes estejam acessíveis com o mínimo de cliques possível, além de otimizar o uso de palavras-chave relevantes nos textos de âncora. Esta ferramenta não só melhora o SEO técnico, mas também contribui significativamente para a estratégia de conteúdo e link building do site.

## O Que Você Vai Aprender
- Como extrair e preparar dados do Screaming Frog e Google Search Console.
- Como instalar e executar este script para análise de rotas de usuário.
- Como interpretar os resultados para fazer ajustes estratégicos em seu site.

## Preparando os Dados
Antes de executar o script, prepare os dados necessários seguindo estes passos:

### Screaming Frog
1. Realize uma auditoria completa do site.
2. Acesse a aba "Internal", selecione todas as linhas, clique com o botão direito e selecione "Inlinks" no menu "Export".
3. Salve o arquivo como `inlinks.csv` na mesma pasta do script.

### Google Search Console
1. Acesse a Visão Geral, clique em "Relatório completo" na sessão de Desempenho.
2. Clique em exportar > "Baixar Arquivo CSV".
3. Você receberá um arquivo .zip contendo vários CSVs. Extraia e utilize apenas o arquivo `Páginas.csv`.

## Instalação do Script
Certifique-se de que Python está instalado no seu sistema. Se necessário, instale-o a partir do [site oficial do Python](https://www.python.org/downloads/). Além disso, instale as bibliotecas necessárias usando o comando:

    pip install pandas networkx

Salve o script em um arquivo Python (por exemplo, `path_analysis.py`) na mesma pasta dos arquivos CSV.

## Executando o Script

Para executar o script, abra o terminal ou prompt de comando e execute:

    python path_analysis.py

Siga as instruções no terminal para inserir os nomes dos arquivos e as URLs necessárias. O script processará os dados e gerará um arquivo `.html` com a análise completa e um arquivo `.csv` com todas as rotas possíveis.

## Interpretação dos Resultados

Os resultados são apresentados de forma a entender rapidamente as rotas mais eficientes e identificar gargalos na navegação do site. Informações como origem e destino das URLs, profundidade dos links e textos de âncora utilizados serão disponibilizados.

## Ajustes Estratégicos

Utilize as informações do relatório para realizar ajustes como reduzir a profundidade de links importantes e otimizar textos de âncora para melhorar a relevância e o ranking de palavras-chave específicas.

## Conclusão

Este script oferece uma visão clara de como os usuários alcançam suas páginas mais importantes, permitindo otimizações que podem melhorar significativamente a experiência do usuário e o desempenho nos motores de busca.


## Contatos e Redes Sociais

<p align="left" dir="auto">
  <a href="https://www.marcostadeu.com.br/" alt="Website">
    <img src="https://img.shields.io/badge/Website-006E93?style=flat-square&logo=wordpress&logoColor=white">
  </a>
  <a href="mailto:marcostadeu.seo@gmail.com" alt="Gmail">
    <img src="https://img.shields.io/badge/-Gmail-FF0000?style=flat-square&labelColor=FF0000&logo=gmail&logoColor=white">
  </a>
  <a href="https://www.linkedin.com/in/marcos-tadeu-especialista-em-seo/" alt="LinkedIn">
    <img src="https://img.shields.io/badge/-Linkedin-0e76a8?style=flat-square&logo=Linkedin&logoColor=white">
  </a>
  <a href="https://www.instagram.com/seo.marcostadeu/" alt="Instagram">
    <img src="https://img.shields.io/badge/-Instagram-DF0174?style=flat-square&labelColor=DF0174&logo=instagram&logoColor=white">
  </a>
  <a href="https://buymeacoffee.com/seomarcos" alt="Buy Me a Coffee">
    <img src="https://img.shields.io/badge/-Buy%20Me%20a%20Coffee-FF813F?style=flat-square&labelColor=FF813F&logo=buy-me-a-coffee&logoColor=white">
  </a>
</p>
