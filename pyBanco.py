import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import datetime
import mysql.connector

# Configurações do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "login"
}

def conectar_banco_dados():
    try:
        conexao = mysql.connector.connect(**db_config)
        return conexao
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {erro}")
        return None

def verificar_login():
    usuario = usuario_entry.get()
    senha = senha_entry.get()

    conexao = conectar_banco_dados()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM user WHERE NOME = %s AND SENHA = %s", (usuario, senha))
        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
            messagebox.showinfo("Login", "Bem-vindo!")
            mostrar_tela("principal")
            return resultado  # Retorna os dados do usuário para verificar o ID
        else:
            messagebox.showerror("Login", "Usuário ou senha incorretos.")
            return None

def cadastrar_usuario():
    usuario = usuario_cadastro_entry.get()
    senha = senha_cadastro_entry.get()

    conexao = conectar_banco_dados()
    if conexao:
        cursor = conexao.cursor()
        query = "INSERT INTO user (NOME, SENHA) VALUES (%s, %s)"
        try:
            cursor.execute(query, (usuario, senha))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            mostrar_tela("login")
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {erro}")
        finally:
            cursor.close()
        conexao.close()

def cadastrar_empresa():
    nome_empresa = nome_empresa_entry.get()
    cnpj = cnpj_entry.get()
    num_funcionarios = num_funcionarios_entry.get()
    telefone = telefone_entry.get()
    endereco = endereco_entry.get()

    conexao = conectar_banco_dados()
    if conexao:
        cursor = conexao.cursor()
        query = "INSERT INTO empresa (nome, cnpj, funcionarios, telefone, endereco) VALUES (%s, %s, %s, %s, %s)"
        try:
            cursor.execute(query, (nome_empresa, cnpj, num_funcionarios, telefone, endereco))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Empresa cadastrada com sucesso!")
            mostrar_tela("login")
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro ao cadastrar empresa: {erro}")
        finally:
            cursor.close()
        conexao.close()

def mostrar_tela(tela):
    # Esconde todos os frames
    for frame in frames.values():
        frame.pack_forget()
    # Mostra o frame solicitado
    frames[tela].pack(fill="both", expand=True)

# Configuração da janela principal
janela = tk.Tk()
janela.title("Ponto Fácil - Login")
janela.geometry("400x300")
janela.configure(bg="#e0f2f7")

frames = {}

# Tela de Login
frame_login = tk.Frame(janela, bg="#e0f2f7")
frames["login"] = frame_login
frame_login.pack(fill="both", expand=True)

tk.Label(frame_login, text="Usuário:", bg="#e0f2f7").pack()
usuario_entry = tk.Entry(frame_login)
usuario_entry.pack()

tk.Label(frame_login, text="Senha:", bg="#e0f2f7").pack()
senha_entry = tk.Entry(frame_login, show="*")
senha_entry.pack()

tk.Button(frame_login, text="Login", command=verificar_login, bg="#4caf50", fg="white").pack(pady=10)
tk.Button(frame_login, text="Cadastro", command=lambda: mostrar_tela("cadastro"), bg="#2196f3", fg="white").pack(pady=5)
tk.Button(frame_login, text="Cadastro de Empresa", command=lambda: mostrar_tela("cadastro_empresa"), bg="#ff9800", fg="white").pack(pady=5)

# Tela Cadastro de Usuário
frame_cadastro = tk.Frame(janela, bg="#e0f2f7")
frames["cadastro"] = frame_cadastro

tk.Label(frame_cadastro, text="Usuário:", bg="#e0f2f7").pack()
usuario_cadastro_entry = tk.Entry(frame_cadastro)
usuario_cadastro_entry.pack()

tk.Label(frame_cadastro, text="Senha:", bg="#e0f2f7").pack()
senha_cadastro_entry = tk.Entry(frame_cadastro, show="*")
senha_cadastro_entry.pack()

tk.Button(frame_cadastro, text="Cadastrar", command=cadastrar_usuario, bg="#4caf50", fg="white").pack(pady=10)
tk.Button(frame_cadastro, text="Voltar", command=lambda: mostrar_tela("login"), bg="#ff9800", fg="white").pack(pady=5)

# Tela Cadastro de Empresa
frame_cadastro_empresa = tk.Frame(janela, bg="#e0f2f7")
frames["cadastro_empresa"] = frame_cadastro_empresa

tk.Label(frame_cadastro_empresa, text="Nome da Empresa:", bg="#e0f2f7").pack()
nome_empresa_entry = tk.Entry(frame_cadastro_empresa)
nome_empresa_entry.pack()

tk.Label(frame_cadastro_empresa, text="CNPJ:", bg="#e0f2f7").pack()
cnpj_entry = tk.Entry(frame_cadastro_empresa)
cnpj_entry.pack()

tk.Label(frame_cadastro_empresa, text="Número de Funcionários:", bg="#e0f2f7").pack()
num_funcionarios_entry = tk.Entry(frame_cadastro_empresa)
num_funcionarios_entry.pack()

tk.Label(frame_cadastro_empresa, text="Telefone:", bg="#e0f2f7").pack()
telefone_entry = tk.Entry(frame_cadastro_empresa)
telefone_entry.pack()

tk.Label(frame_cadastro_empresa, text="Endereço:", bg="#e0f2f7").pack()
endereco_entry = tk.Entry(frame_cadastro_empresa)
endereco_entry.pack()

tk.Button(frame_cadastro_empresa, text="Cadastrar Empresa", command=cadastrar_empresa, bg="#4caf50", fg="white").pack(pady=10)
tk.Button(frame_cadastro_empresa, text="Voltar", command=lambda: mostrar_tela("login"), bg="#ff9800", fg="white").pack(pady=5)

# Tela Principal
frame_principal = tk.Frame(janela, bg="#e0f2f7")
frames["principal"] = frame_principal

tk.Label(frame_principal, text="Bem-vindo à Tela Principal", font=("Arial", 14), bg="#e0f2f7").pack(pady=10)
tk.Button(frame_principal, text="Espelho de Ponto", command=lambda: mostrar_tela("espelho_ponto"), bg="#2196f3", fg="white").pack(pady=10)
tk.Button(frame_principal, text="Bater Ponto", command=lambda: mostrar_tela("bater_ponto"), bg="#4caf50", fg="white").pack(pady=10)
tk.Button(frame_principal, text="Sair", command=lambda: mostrar_tela("login"), bg="#ff9800", fg="white").pack(pady=10)

# Tela Espelho de Ponto
frame_espelho_ponto = tk.Frame(janela, bg="#e0f2f7")
frames["espelho_ponto"] = frame_espelho_ponto

tk.Button(frame_espelho_ponto, text="Voltar", command=lambda: mostrar_tela("principal"), bg="#ff9800", fg="white").pack(anchor="nw", padx=10, pady=10)

# Tela Bater Ponto
frame_bater_ponto = tk.Frame(janela, bg="#e0f2f7")
frames["bater_ponto"] = frame_bater_ponto

def registrar_ponto():
    try:
        conexao = conectar_banco_dados()
        if conexao:
            cursor = conexao.cursor()
            data_hora = datetime.datetime.now()
            query = "INSERT INTO ponto (data) VALUES (%s)"
            cursor.execute(query, (data_hora,))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Ponto registrado com sucesso!")
            cursor.close()
        conexao.close()
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro", f"Erro ao registrar ponto: {erro}")

tk.Label(frame_bater_ponto, text="Clique abaixo para registrar seu ponto", bg="#e0f2f7").pack(pady=10)
tk.Button(frame_bater_ponto, text="Registrar Ponto", command=registrar_ponto, bg="#4caf50", fg="white").pack(pady=10)
tk.Button(frame_bater_ponto, text="Voltar", command=lambda: mostrar_tela("principal"), bg="#ff9800", fg="white").pack(pady=10)

janela.mainloop()