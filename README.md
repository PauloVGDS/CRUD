# CRUD
Interface de login com opção de registro e janela de administrador.
Depois de quebra a cabeça com o Tkinter fiz essa interface, espero que tenha ficado minimamente bom em algum sentido kkkk
Estou aprendendo a usar essa plataforma também, se alguém estiver vendo isso e tiver sugestões de como eu posso melhorar o meu código ou até de como usar o github ajudaria muito.
# Como isso roda?
O código é interface de login, registro e administrador para um sistema de informação. A interface é desenvolvida utilizando o módulo tkinter para criar a interface gráfica e o módulo ttkbootstrap para adicionar estilos à interface. Além disso, o módulo mysql.connector é utilizado para se conectar a um banco de dados MySQL e realizar operações de inserção, atualização e consulta de dados.

A interface possui três janelas: a janela de login, a janela de registro e a janela de administrador. A janela de login possui dois campos de entrada para o usuário inserir o seu email e senha, e um botão para enviar essas informações ao servidor. A janela de registro possui campos para o usuário inserir o seu nome, sobrenome, email e senha, e um botão para enviar essas informações ao servidor. A janela de administrador possui campos para o usuário inserir o ID ou Email do usuário que deseja alterar, e um botão para visualizar ou apagar essas informações do servidor.

# Funções
A janela é inicialmente criada vazia e as funções main_log_frame, main_reg_frame e main_adm_frame criam um frame com os campos de cada janela.

As funções reg_msg(), log_msg() e adm_msg() são chamadas quando o usuário clica nos respectivos botões de enviar nas janelas de registro, login e administrador. Essas funções verificam se os dados inseridos pelo usuário são válidos e, se forem, enviam as informações ao banco de dados MySQL para serem armazenadas ou atualizadas. As funções também exibem mensagens na tela para informar o usuário sobre o resultado das operações.

A função del_adm é a função responsável por apagar um registro na janela de admistrador.

As funções log(), reg() e adm() são chamadas quando eu quero alternar entre janelas, onde ela destroi o frame criado pelas funções main_log_frame, main_reg_frame e main_adm_frame e em seguida chama uma dessas funções para criar outro frame no lugar.
Por exemplo a função reg(), ela destroi o frame de login e chama a função(main_reg_frame) que cria o frame de registro.

A função show_senhas() controla a checkbox de mostrar a senha.

# Um erro só que funciona kkkk
A função log() tem uma peculiaridade pois ela funciona de uma forma que pra mim não era pra funcionar, eu estava tendo um erro quando eu queria alternar entre as janelas, quando eu alternava entre duas janelas(entre a janela de registro e login por exemplo) funcionava perfeitamente, porém, se eu alternasse entre as três janelas existentes ele aparentemente não entrava na "except NameError" logo não destruia o frame que eu queria(o de registro) então ele ficava criando frames na mesma janela sem apagar o anteriro enchendo o janela e bagunçando tudo, então, por acaso eu coloquei entro do "finally" o comando pra destruir o frame de registro novamente e isso fez funcionar, eu não entendi o porque mas depois disso eu consegui alternar entre as janelas tranquilamente.
# Visual

![image](https://user-images.githubusercontent.com/122188615/214656912-193638c3-7ef9-4a6f-9055-d4b35902f363.png)

![image](https://user-images.githubusercontent.com/122188615/214656924-174928cc-f665-4c4f-bb5c-407179eaa34a.png)

![image](https://user-images.githubusercontent.com/122188615/214656935-0b1fc179-4664-4339-9e20-a16f4e93d911.png)
