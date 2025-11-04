# zoho-crm-etl


Script em Python para integração automatizada entre o Zoho CRM e um banco de dados MySQL. Ele faz a autenticação via API (OAuth2), vai extrair registros de tarefas do Zoho e insere em tabelas locais, mantendo o banco de dados atualizado.

Principais recursos utilizados: 1 - Conexão com a API Zoho CRM usando refresh token 2 - Paginação automática de resultados (a API pega 200 linhas por página) 3 - Tratamento de campos aninhados (como Owner, Solicitante, entre outros.) 4 - Limpeza e inserção dos dados no banco

Tecnologias utilizadas:

Python
Requests
MySQL Connector
Zoho CRM API
Como usar: Configure suas credenciais do Zoho e MySQL nas variáveis no topo do script. Execute: python nome_do_arquivo.py Dessa forma, os dados irão ser baixados e inseridos automaticamente no banco de dados, onde o mesmo será atualizado.
