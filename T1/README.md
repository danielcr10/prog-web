# T1 de programação web
Participantes: Daniel Cunha Rios
## Instalação
Para rodar o servidor basta baixar os arquivos do repositório, personalizar o arquivo de configuração e executar o servidor.
```bash
$ git clone https://github.com/danielcr10/prog-web.git
# Para editar as configurações do servidor
$ vim config.py
$ python3 servidor.py
```
No meu exemplo, as páginas estão hospedadas na pasta pags, dentro do próprio repositório

## O que funcionou
O servidor atende somente ao tipo de requisição GET e de arquivos html, js, jpeg, jpg, png, gif conforme solicitado no trabalho.
Como ponto fundamental também, o servidor suporta multiplas conexões simultâneas conforme solicitado e testado através de um sleep em testes para simular conexões simultâneas através de dois navegadores distintos disparando requisições. 
Como forma de garantir a qualidade das configurações que serão incluidas pelo usuários, foram realizadas validações das mesmas de acordo com as especificações do trabalho e dos comentários documentados no pŕoprio módulo de configuração, arquivo config.py.
Mediante aos testes realizados, todos os erros foram capturados, tratados e enviados para o arquivo de erros previamente definido.
Todas os arquivos solicitados e não encontrados emitem um erro como resposta enviando um código 404.

## O que não funcionou
De tudo que foi testado por mim e solicitado no trabalho, não consegui encontrar problemas que não consegui solucionar.