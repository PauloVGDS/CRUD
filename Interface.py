import tkinter
from tkinter import IntVar, RIGHT, LEFT
from ttkbootstrap import Frame, Button, LabelFrame, Label, Entry, SUCCESS, DANGER, PRIMARY, INFO, Checkbutton, OUTLINE, \
    Window, Spinbox, WARNING
import mysql.connector

var1 = IntVar


def reg_msg():  # Função que controla as mensagens da janela de registros
    # Guarda os valores em variáveis
    nome = str(f'{nome_entry.get()} {sobnome_entry.get()}').strip()
    gmail = email.get().strip()
    chave = senha.get().strip()
    confirm_chave = confirm_senha.get().strip()
    # Condições para caso as informações estejam incorretas
    if chave != confirm_chave:
        msg['text'] = 'As senhas não batem!'
    elif len(chave) < 4:
        msg['text'] = 'Por favor, senhas maiores que 4 caracteres!'
        janela.geometry('320x435')
    elif len(gmail) < 13 or '@gmail.com' not in gmail or len(nome) <= 3:
        msg['text'] = 'Por favor, insira um email e/ou nome válido!'
        janela.geometry('335x450')
    else:
        # Se as informações concordarem ele dá uma mensagem de sucesso e conecta no servidor
        msg['text'] = 'Registro efetuado com sucesso!'
        # Conecta ao servidor MySQL
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="programa"
        )

        # Cria um cursor para executar as consultas SQL
        cursor = conexao.cursor()

        # Condição para caso eu não esteja a fazer um teste
        if nome != 'teste' and gmail != 'teste@gmail.com' and chave != 'teste':
            try:  # Executa a consulta SQL para inserir os dados do usuário no banco de dados
                # Comando para inserir os valores na database
                cursor.execute("INSERT INTO registros (nome, email, senha) VALUES (%s, %s, %s)", (nome, gmail, chave))
                # Comando para extrair apenas o ID do registro criado(não foi usado)
                cursor.execute("SELECT id FROM registros WHERE email = %s", (gmail,))

                # Armazena o resultado da consulta em uma variável
                resultado = cursor.fetchone()
            # O email está configurado para ser único, logo, caso um email repetido seja inserido ele retorna essa mensagem
            except mysql.connector.errors.IntegrityError:
                msg['text'] = 'Esse email já foi registrado!\nPor favor, faça login ou ultilize outro email.'
                janela.geometry('320x460')
                pass

        else:
            # Mensagem de sucesso do teste
            msg['text'] = 'Teste Realizado!'
        # Fecha a conexão com o servidor MySQL
        conexao.close()


def log_msg():  # Função que controla as mensagens da janela de login
    # Guarda os valores em variáveis
    gmail = email_entry.get().strip()
    senha = senha_entry.get().strip()
    # Senha de administrador
    if gmail == 'admin' and senha == '':
        adm()
    else:
        # Conecta ao servidor MySQL
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="programa"
        )

        # Cria um cursor para executar as consultas SQL
        cursor = conexao.cursor()

    # Executa a consulta SQL para inserir os dados do usuário no banco de dados
        # Comando para selecionar informações na database
        cursor.execute("SELECT * FROM registros WHERE email = %s and senha = %s", (gmail, senha))

        # Armazena o resultado da consulta em uma variável
        resultado = cursor.fetchone()
        # Condição para caso o email exista
        if resultado is not None:
            msg['text'] = f"Logado com sucesso!\n Bem vindo {resultado[3]}."
            janela.geometry("270x350")
        else:
            # Caso o email não exista ele retorna essa mensagem
            msg['text'] = 'Login e/ou senha incorretos\nRegistre caso não tenha conta.'
            janela.geometry("270x350")
        # Fecha a conexão com o servidor MySQL
        conexao.close()


def adm_msg():  # Função que controla as mensagens da janela de administrador
    # Variáveis globais usadas em outras funções
    global id_result, gmail_result
    id_result = id_spin.get()
    gmail_result = gm_entry.get()
    # Conecta ao servidor MySQL
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="programa"
    )

    # Cria um cursor para executar as consultas SQL
    cursor = conexao.cursor()

    # Executa a consulta SQL para inserir os dados do usuário no banco de dados
    cursor.execute("SELECT * FROM registros WHERE id = %s or email = %s", (id_result, gmail_result))

    # Armazena o resultado da consulta em uma variável
    resultado = cursor.fetchone()
    # Fecha a conexão com o servidor MySQL
    conexao.close()
    # Se o resultado não for nulo(vazio) ele atualiza a mensagem
    if resultado is not None:
        msg_adm['text'] = f'ID:{resultado[0]}\nNome:{resultado[3]}\nEmail:{resultado[1]}\nSenha:{resultado[2]}'
        janela.geometry('420x451')
    else:
        msg_adm['text'] = 'ID e/ou Email inexistente!'
        janela.geometry('420x411')


def del_adm():  # Função que localiza e(caso deseje) deleta as informações

    # Conecta ao servidor MySQL
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="programa"
    )

    # Cria um cursor para executar as consultas SQL
    cursor = conexao.cursor()

    # Armazena o resultado da consulta em uma variável
    resultado = cursor.fetchone()

    # Comando para deletar a informação
    cursor.execute("DELETE FROM registros WHERE id = %s OR email = %s", (id_result, gmail_result))

    # Fecha a conexão com o servidor MySQL
    conexao.close()
    # Se o resultado não for nulo ele atualiza a mensagem de exclusão
    if resultado is not None:
        msg_adm['text'] = f'{id_result} apagado com sucesso!'


def reg():  # Função para destruir o frame de login e chamar a função que contem o frame de registro
    # Destroi o frame de login
    main_login_frame.destroy()
    # Chama a função que contém o frame de registro
    main_reg_frame()


def log():  # Função para destruir o frame de registro ou frame de administrador e chamar a função que contém o frame de login
    try:
        # Tenta destruir o frame de login
        main_admin_frame.destroy()
    # Excesão caso esteja em um frame diferente do de administrador
    except NameError:
        main_register_frame.destroy()
    # Por fim ele chama a função que contém o frame de login
    finally:
        main_register_frame.destroy()  # Essa linha simplismente faz o código funcionar, não sei o porque exatamente.
        main_log_frame()


def adm():  # Função que destroi o frame de login e chama a função que contém o frame de administrador
    # Destroi o frame de login
    main_login_frame.destroy()
    # Chama a função que contém o fram de administrador
    main_adm_frame()


def show_senhas():  # Função para controlar caso eu queira ou não mostrar a senha na janela de login
    # Variável global que uso em outra função
    global var1
    # Condição para caso eu queira ou não ver a senha
    if var1 == 1:
        # Se for 1 então ele esconde a senha e determina a variável como 0
        senha_entry['show'] = '*'
        var1 = 0
    else:
        # Se for 0 então mostra a senha e determina a variável como 1
        senha_entry['show'] = ''
        var1 = 1


def main_log_frame():  # Função que contém o frame de registro
    # Variáveis globai que usamos em outras funções
    global main_login_frame, janela, email_entry, senha_entry, b_log, msg
    # Parametro para configurar o tamanho da janela
    janela.geometry('270x340')
    # Frame Principal
    main_login_frame = Frame(master=janela, padding=10)
    main_login_frame.pack(expand=True, fill='both')

    # Título
    titulo_frame = LabelFrame(master=main_login_frame) # Frame do Título
    titulo_frame.grid(row=0, column=0)
    Label(text='Interface de Login', master=titulo_frame, font='Calibri 20 bold',style=PRIMARY).pack()  # Label do Título

    # Email
    email_frame = Frame(master=main_login_frame, padding=15)  # Frame do Email
    email_frame.grid(row=1, column=0)
    Label(text='Login: ', master=email_frame, font='Calibri 20 bold', style=PRIMARY).pack(side=LEFT)  # Label do Email
    email_entry = Entry(master=email_frame)  # Entry do Email
    email_entry.pack(side=RIGHT)

    # Senha
    senha_frame = Frame(master=main_login_frame, padding=15)  # Frame da Senha
    senha_frame.grid(row=2, column=0)
    Label(text='Senha:', master=senha_frame, font='Calibri 20 bold', style=PRIMARY).pack(side=LEFT)  # Label da senha
    senha_entry = Entry(master=senha_frame, show='*')  # Entry da senha
    senha_entry.pack(side=RIGHT)

    # Mostrar senha
    show_senha = Frame(master=main_login_frame)  # Frame do Checkbutton
    show_senha.grid(row=3, column=0)
    Checkbutton(master=show_senha, text='Mostrar senha', style=SUCCESS, variable=var1, onvalue=1, offvalue=0,command=show_senhas).pack() # CheckButton de mostrar ou não a senha

    # Menssagem
    men = Frame(main_login_frame) # Frame das mensagens
    men.grid(row=4)
    msg = Label(men, text='Caso não tenha conta, registre-se!', font='Calibri 12 bold', style=INFO) # Label das mensagens
    msg.pack(side=LEFT, pady=10)

    # Botões
    botoes_frame = LabelFrame(master=main_login_frame, padding=10)  # Frame dos Botões
    botoes_frame.grid(row=5, column=0)
    b_login = Button(text='Logar', style=(PRIMARY, OUTLINE), master=botoes_frame, command=log_msg)  # Botão de Login
    b_login.pack(side=LEFT, padx=10)
    b_sair = Button(text='Sair', style=(DANGER, OUTLINE), master=botoes_frame,command=janela.destroy)  # Botão para Sair
    b_sair.pack(side=RIGHT, padx=10)
    b_log = Button(text='Registrar', style=(PRIMARY, OUTLINE), master=botoes_frame, command=reg)  # Botão de Registro
    b_log.pack()


def main_reg_frame():  # Função que contém o frame de registro
    # Variáveis globais que usamos em outras funções
    global main_register_frame, nome_entry, sobnome_entry, email, senha, confirm_senha, msg, b_reg
    janela.geometry('305x450')
    # Frame Principal
    main_register_frame = Frame(master=janela, padding=10)
    main_register_frame.pack(expand=True, fill='both')
    # Título
    titulo_frame = LabelFrame(master=main_register_frame) # Frame de Título
    titulo_frame.grid(row=0, column=0)
    Label(text='Interface de Registro', master=titulo_frame, font='Arial 20 bold',style=PRIMARY).pack()  # Label do Título

    # Nome
    nome_frame = Frame(master=main_register_frame, padding=10)  # Frame do Nome
    nome_frame.grid(row=1, column=0)
    Label(text='Nome:', master=nome_frame, font='Arial 15 bold', style=PRIMARY).pack(side=LEFT)  # Label do Nome
    nome_entry = Entry(master=nome_frame)  # Entry do Nome
    nome_entry.pack(side=RIGHT, ipadx=33)

    # Sobrenome
    sobnome_frame = Frame(master=main_register_frame, padding=10)  # Frame da Sobrenome
    sobnome_frame.grid(row=2, column=0)
    Label(text='Sobrenome:', master=sobnome_frame, font='Arial 15 bold', style=PRIMARY).pack(side=LEFT)  # Label da Sobrenome
    sobnome_entry = Entry(master=sobnome_frame)  # Entry da Sobrenome
    sobnome_entry.pack(side=RIGHT, ipadx=6)

    # Email
    email_frame = Frame(main_register_frame, padding=10)  # Frame do Email
    email_frame.grid(row=3)
    Label(email_frame, text=' Email:', font='Arial 15 bold', style=PRIMARY).pack(side=LEFT)  # Label do Email
    email = Entry(email_frame)  # Entry do Email
    email.pack(ipadx=32)

    # Senha
    senha_frame = Frame(main_register_frame, padding=10)  # Frame da senha
    senha_frame.grid(row=4)
    Label(senha_frame, text='Senha:', font='Arial 15 bold', style=PRIMARY).pack(side=LEFT)  # Label da senha
    senha = Entry(senha_frame)  # Entry da Senha
    senha.pack(ipadx=31)

    # Confirmar Senha
    confirm_senha_frame = Frame(main_register_frame, padding=10) # Frame da confimação da senha
    confirm_senha_frame.grid(row=5)
    Label(confirm_senha_frame, text='Confirmação:', font='Arial 15 bold', style=PRIMARY).pack(side=LEFT)  # Label da confimação da senha
    confirm_senha = Entry(confirm_senha_frame, show='')  # Entry da confimação da senha
    confirm_senha.pack()
    # Botões
    botoes_frame = LabelFrame(master=main_register_frame, padding=10)  # Frame dos Botões
    botoes_frame.grid(row=7, column=0)
    b_reg = Button(text='Registrar', style=(PRIMARY, OUTLINE), master=botoes_frame, command=reg_msg)  # Botão de Login
    b_reg.pack(side=LEFT, padx=10)
    b_sair = Button(text='Voltar', style=(PRIMARY, OUTLINE), master=botoes_frame, command=log)  # Botão para Sair
    b_sair.pack(side=RIGHT, padx=10)

    # Menssagem
    msg_frame = Frame(main_register_frame)  # Frame da mensagem
    msg_frame.grid(row=6)
    msg = Label(msg_frame, text='Confirme sua senha.\nPreencha todas as informações a cima!', font='Calibri 12 bold',style=INFO) # Label da mensagem
    msg.pack(side=LEFT, pady=10)


def main_adm_frame(): # Função que contém o frame de administrador
    # Variáveis globais que usamos em outras funções
    global main_admin_frame, janela, b_busca, b_del, b_volt, id_spin, gm_entry, msg_adm
    janela.geometry('420x411')
    # Frame Principal
    main_admin_frame = Frame(master=janela, padding=10)
    main_admin_frame.pack(expand=True, fill='both')

    # Título
    titulo_frame = LabelFrame(master=main_admin_frame) # Frame do Título
    titulo_frame.grid(row=0, column=0)
    Label(text='Interface de Administrador', master=titulo_frame, font='Calibri 20 bold',style=PRIMARY).pack()  # Label do Título

    # Menssagem - 1
    men = Frame(main_admin_frame)  # Frame da Menssagem 1
    men.grid(row=1, column=0)
    msg = Label(men, text='Interface do Administrador.', font='Calibri 12 bold', style=WARNING)  # Label da Mensagem 1
    msg.pack(side=LEFT, pady=10)

    # Menssagem - 2
    men2 = Frame(main_admin_frame)  # Frame da Menssagem 2
    men2.grid(row=2, column=0)
    msg2 = Label(men2, text='Digite o EMAIL do registro para mostrar suas informações.', font='Calibri 12 bold')   # Label da Mensagem 2
    msg2.pack(side=LEFT, pady=10)

    # Caixa de ID - 1
    id_frame1 = Frame(main_admin_frame) # Frame da Caixa de ID 1
    id_frame1.grid(row=3)
    gm_entry = Entry(id_frame1, style=INFO, width=40) # Entry da Caixa de ID 1
    gm_entry.pack()

    # Menssagem - 3
    men3 = Frame(main_admin_frame)  # Frame da Mensagem 3
    men3.grid(row=4, column=0)
    msg3 = Label(men3, text='Ou o ID de registro.', font='Calibri 12 bold')  # Label da Mensagem 3
    msg3.pack(side=LEFT, pady=10)

    # Caixa de ID - 2
    id_frame2 = Frame(main_admin_frame, padding=5)  # Frame da Caixa de ID - 2
    id_frame2.grid(row=5)
    id_spin = Spinbox(id_frame2, from_=1, to=999, style=INFO, width=3)  # Spinbox da Caixa de ID - 2
    id_spin.pack()

    # Informações dos Registros
    info_frame = LabelFrame(main_admin_frame)  # Frame das Informações dos Registros
    info_frame.grid(row=6)
    msg_adm = Label(info_frame, text='As informações aparecerão aqui', style=SUCCESS, font='Arial 10 bold')  # Label das Informações dos Registros
    msg_adm.pack()

    # Botões
    botoes_frame = LabelFrame(master=main_admin_frame, padding=10)  # Frame dos Botões
    botoes_frame.grid(row=9, column=0)
    b_busca = Button(text='Buscar', style=(PRIMARY, OUTLINE), master=botoes_frame, command=adm_msg)  # Botão de Buscar registros
    b_busca.pack(side=LEFT, padx=10)
    b_del = Button(text='Deletar', style=(DANGER, OUTLINE), master=botoes_frame, command=del_adm)  # Botão de Deletar um registro
    b_del.pack(side=LEFT, padx=10)
    b_volt = Button(text='Voltar', style=(PRIMARY, OUTLINE), master=botoes_frame, command=log)  # Botão para Voltar para a janela de login
    b_volt.pack(side=RIGHT, padx=10)

    # Menssagem - 4
    men4 = Frame(main_admin_frame)  # Frame da Mensagem 4
    men4.grid(row=10, column=0)
    msg4 = Label(men4, text='Registros não podem ser restaurados caso apagados.', font='Calibri 12 bold', style=DANGER)  # Label da Mensagem 4
    msg4.pack(side=LEFT, pady=10)


janela = Window(themename='cyborg', iconphoto='Arvore.ico', title='Inferace')  # Aqui é onde a janela é criada inicialmente

main_log_frame()  # A primeira função que é chamada que contém o frame de login(que é o inicial, pode ser alterado)

janela.mainloop()  # Função para manter a janela em loop
