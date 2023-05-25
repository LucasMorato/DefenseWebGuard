<h1>DefenseWebGuard</h1>
<h2>Visão geral</h2>
<p>Esse script em Python desenvolvido por mim é uma ferramenta poderosa desenvolvida para proteger a internet, ajudando a identificar e alertar proprietários de sites que possuem falhas de segurança no WordPress. Com sua automação inteligente, o script simplifica todo o processo de busca, encontra os endereços de e-mail dos proprietários e envia automaticamente os alertas com apenas algumas configurações e uma linha de comando. É necessário ter o wpscan instalado e um token em sua máquina Linux.</p>
<h2>Funcionamento</h2>
<p>O script realiza as seguintes etapas principais:</p>
<ol>
  <li>Realiza uma pesquisa no Google em páginas consecutivas (1 a 2) utilizando a URL de pesquisa construída com base nos argumentos fornecidos.</li>
  <li>Extrai os links dos resultados da pesquisa.</li>
  <li>Armazena URLs únicas, removendo duplicatas e ignorando URLs do Google.</li>
  <li>Aguarda por alguns segundos entre as solicitações para evitar bloqueios e respeitar as políticas do Google.</li>
  <li>Imprime uma mensagem de escaneamento antes de começar a verificar os sites.</li>
  <li>Para cada site da lista de URLs únicas:
    <ul>
      <li>Extrai o nome do site a partir da URL.</li>
      <li>Executa o comando curl para obter o conteúdo HTML do site e salva em um arquivo.</li>
      <li>Procura por emails no conteúdo do arquivo utilizando expressões regulares.</li>
      <li>Armazena os emails únicos encontrados agrupados por URL.</li>
      <li>Remove o arquivo de saída.</li>
    </ul>
  </li>
  <li>Imprime os emails encontrados agrupados por URL, caso existam.</li>
  <li>Para cada site que possui emails encontrados:
    <ul>
      <li>Extrai o nome do site a partir da URL.</li>
      <li>Executa o comando wpscan no site, utilizando os emails como parâmetro de busca.</li>
      <li>Salva o relatório do wpscan em um arquivo de texto.</li>
      <li>Atualiza a barra de progresso indicando o progresso do wpscan.</li>
    </ul>
  </li>
</ol>
<h2>Dependências</h2>
<p>O script possui as seguintes dependências:</p>
<ul>
  <li>Python 3.x</li>
  <li>Biblioteca requests</li>
  <li>Biblioteca beautifulsoup4</li>
  <li>Biblioteca argparse</li>
  <li>Biblioteca subprocess</li>
  <li>Biblioteca os</li>
  <li>Biblioteca re</li>
  <li>Biblioteca colorama</li>
  <li>Biblioteca tqdm</li>
</ul>
<h2>Modo de uso</h2>
<ol>
  <li>Clone o repositório que contém o script ou baixo script.</li>
  <li>Certifique-se de ter todas as dependências mencionadas instaladas.</li>
  <li>Abra um terminal e navegue até o diretório onde o script está localizado.</li>
  <li>Execute o seguinte comando para exibir a ajuda e ver os argumentos necessários:
      </div><div>python script.py --help  </div></div>
  </pre>
  </li>
  <li>Utilize os seguintes argumentos para executar o script:
    <ul>
      <li>--site: Domínio do site a ser pesquisado (por exemplo, "br").</li>
      <li>--text: Texto a ser procurado nos resultados da pesquisa (por exemplo, "escola").</li>
    </ul>

  <li>Aguarde até que o script conclua a pesquisa, verificação de emails e execução do wpscan.</li>
  <li>Os resultados serão exibidos no terminal, incluindo os emails encontrados agrupados por URL e o progresso do wpscan em cada site.</li>
</ol>
<p>É importante ressaltar que o script pode levar algum tempo para ser concluído, dependendo do número de páginas de pesquisa e sites a serem verificados. Certifique-se de respeitar as políticas e termos de uso do Google e dos sites acessados pelo script.</p>

Exemplo:

```
python script.py --site br --text escola
```  
