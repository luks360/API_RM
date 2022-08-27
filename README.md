# Como começar

Primeiro, baixe todas as dependências da API com o comando: `pip install -r requeriments.txt`;

Segundo, crie um banco de dados e use o arquivo **schema.sql** para criar as tabelas dele;

Terceiro, acesse o arquivo **db.py**, mude o valor da variavél **DB_NAME** para o nome do banco de dados que você criou e o valor de **DB_PASS** para a senha do seu usuário do banco de dados;

Depois disso é só iniciar a API com: `python app.py`

Acesse [http://localhost:5000/docs](http://localhost:5000/docs) para testar
