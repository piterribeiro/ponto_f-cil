import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import datetime
import mysql.connector
import hashlib
from cryptography.fernet import Fernet

# --- Configurações ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "login"
TEMPO_PADRAO_PONTOS_MINUTOS = 480

# --- Funções de Banco de Dados ---
def conectar_db():
    try:
        conexao = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        return conexao
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {erro}")
        return None

def executar_query(query, params=None):
    conexao = conectar_db()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute(query, params)
            conexao.commit()
            return cursor
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro no banco de dados: {erro}")
            conexao.rollback()
            return None
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()
    return None

def buscar_um(query, params=None):
    conexao = conectar_db()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchone()
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro no banco de dados: {erro}")
            return None
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()
    return None

# --- Funções de Tela ---
def mostrar_tela(tela_nome):
    for nome, frame in frames.items():
        frame.pack_forget()
    frames[tela_nome].pack(fill="both", expand=True)

# --- Funções de Usuário ---
def verificar_login():
    usuario = usuario_entry.get()
    senha = senha_entry.get()

    if usuario == "empresa" and senha == "123":
        messagebox.showinfo("Login", "Bem-vindo, Empresa!")
        mostrar_tela("empresa_config")
        return

    resultado = buscar_um("SELECT ID FROM user WHERE NOME = %s AND SENHA = %s", (usuario, senha))
    if resultado:
        messagebox.showinfo("Login", "Bem-vindo!")
        mostrar_tela("pos_login")
    else:
        messagebox.showerror("Login", "Usuário ou senha incorretos.")

def cadastrar_usuario(usuario, senha):
    if executar_query("INSERT INTO user (NOME, SENHA) VALUES (%s, %s)", (usuario, senha)):
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        mostrar_tela("login")

# --- Funções de Ponto ---
ultimo_ponto = None
historico_pontos_lista = []  # Lista para simular o histórico de pontos na memória

def registrar_ponto():
    global ultimo_ponto
    agora = datetime.datetime.now()
    horario_ponto = agora.strftime("%H:%M:%S")
    dia_semana = agora.strftime("%A") # Obtém o dia da semana
    data_ponto = agora.strftime("%Y-%m-%d")
    ultimo_ponto = agora

    # Simulação de salvar a batida de ponto no banco de dados
    registro = f"{horario_ponto} - {data_ponto} ({dia_semana})"
    print(f"Ponto registrado às {registro}")
    historico_pontos_lista.append(registro) # Adiciona ao histórico na memória

    if agora.hour >= 19:
        messagebox.showinfo("Ponto Registrado", f"Ponto batido às {horario_ponto} com horas extras. Uma mensagem para o RH será enviada e uma reunião será marcada ao final do mês para verificar todas as horas extras.")
        # Aqui você colocaria a lógica para enviar a mensagem ao RH (pode ser um log, um e-mail, etc.)
    else:
        messagebox.showinfo("Ponto Registrado", f"Seu ponto foi registrado às {horario_ponto}")

    mostrar_tela("tempo_proximo_ponto")
    atualizar_tempo_restante()

def atualizar_tempo_restante():
    if ultimo_ponto:
        proximo_ponto = ultimo_ponto + datetime.timedelta(minutes=TEMPO_PADRAO_PONTOS_MINUTOS)
        tempo_restante = proximo_ponto - datetime.datetime.now()
        horas = tempo_restante.seconds // 3600
        minutos = (tempo_restante.seconds % 3600) // 60
        segundos = tempo_restante.seconds % 60
        tempo_restante_label.config(text=f"Tempo restante: {horas:02d}:{minutos:02d}:{segundos:02d}")
    else:
        tempo_restante_label.config(text="Nenhum ponto registrado.")
    janela.after(1000, atualizar_tempo_restante)

# --- Funções de Empresa ---
def cadastrar_empresa(nome, cnpj, funcionarios, telefone, endereco):
    # Simulação de salvar os dados da empresa no banco de dados
    print(f"Empresa cadastrada: {nome}, CNPJ: {cnpj}")
    messagebox.showinfo("Sucesso", "Empresa cadastrada com sucesso!")
    mostrar_tela("login")

def verificar_acesso_cadastro_empresa():
    tela_login_rh = tk.Toplevel(janela)
    tela_login_rh.title("Login RH")
    tela_login_rh.geometry("300x150")

    tk.Label(tela_login_rh, text="ID RH:").pack()
    id_rh_entry = tk.Entry(tela_login_rh)
    id_rh_entry.pack()

    tk.Label(tela_login_rh, text="Senha RH:").pack()
    senha_rh_entry = tk.Entry(tela_login_rh, show="*")
    senha_rh_entry.pack()

    def logar_rh():
        id_rh = id_rh_entry.get()
        senha_rh = senha_rh_entry.get()
        if id_rh == "199805" and senha_rh == "123":
            tela_login_rh.destroy()
            mostrar_tela("cadastro_empresa")
        else:
            messagebox.showerror("Erro", "ID ou senha incorretos.")

    tk.Button(tela_login_rh, text="Login", command=logar_rh).pack()

# --- Nova Funcionalidade: Histórico de Pontos (Simulado) ---
def mostrar_historico_pontos():
    tela_historico = tk.Toplevel(janela)
    tela_historico.title("Histórico de Pontos")
    tela_historico.geometry("300x200")
    tela_historico.configure(bg="#e0f2f7")

    lista_historico = tk.Listbox(tela_historico)
    for item in historico_pontos_lista:
        lista_historico.insert(tk.END, item)
    lista_historico.pack(padx=10, pady=10)

    tk.Button(tela_historico, text="Fechar", command=tela_historico.destroy).pack(pady=5)

# --- Interface Gráfica ---
janela = tk.Tk()
janela.title("Ponto Fácil")
janela.geometry("350x250")
janela.configure(bg="#e0f2f7")

frames = {}

# Tela de Login
frame_login = tk.Frame(janela, bg="#e0f2f7")
frames["login"] = frame_login
tk.Label(frame_login, text="Usuário:", bg="#e0f2f7").pack()
usuario_entry = tk.Entry(frame_login)
usuario_entry.pack()
tk.Label(frame_login, text="Senha:", bg="#e0f2f7").pack()
senha_entry = tk.Entry(frame_login, show="*")
senha_entry.pack()
tk.Button(frame_login, text="Login", command=verificar_login, bg="#4caf50", fg="white").pack(pady=5)
tk.Button(frame_login, text="Cadastrar", command=lambda: mostrar_tela("cadastro"), bg="#2196f3", fg="white").pack(pady=5)
tk.Button(frame_login, text="Cadastro de Empresas", command=verificar_acesso_cadastro_empresa, bg="#ff9800", fg="white").pack(pady=5)
frame_login.pack(fill="both", expand=True)

# Tela Pós Login (Funcionário)
frame_pos_login = tk.Frame(janela, bg="#e0f2f7")
frames["pos_login"] = frame_pos_login
tk.Label(frame_pos_login, text="O que você gostaria de fazer?", bg="#e0f2f7", font=("Arial", 12)).pack(pady=20)
tk.Button(frame_pos_login, text="Marcar Ponto", command=lambda: mostrar_tela("marcar_ponto"), bg="#4caf50", fg="white").pack(pady=10)
tk.Button(frame_pos_login, text="Histórico de Pontos", command=mostrar_historico_pontos, bg="#2196f3", fg="white").pack(pady=10) # Novo botão
tk.Button(frame_pos_login, text="Voltar", command=lambda: mostrar_tela("login"), bg="#ff9800", fg="white").pack(pady=10)

# Tela Marcar Ponto
frame_marcar_ponto = tk.Frame(janela, bg="#e0f2f7")
frames["marcar_ponto"] = frame_marcar_ponto
tk.Label(frame_marcar_ponto, text="Clique para registrar seu ponto", bg="#e0f2f7").pack(pady=10)
tk.Button(frame_marcar_ponto, text="Registrar Ponto", command=registrar_ponto, bg="#4caf50", fg="white").pack(pady=10)
tk.Button(frame_marcar_ponto, text="Voltar", command=lambda: mostrar_tela("pos_login"), bg="#ff9800", fg="white").pack(pady=5)

# Tela Tempo Próximo Ponto
frame_tempo_proximo_ponto = tk.Frame(janela, bg="#e0f2f7")
frames["tempo_proximo_ponto"] = frame_tempo_proximo_ponto
tk.Label(frame_tempo_proximo_ponto, text="Ponto registrado!", bg="#e0f2f7", font=("Arial", 12)).pack(pady=10)
tempo_restante_label = tk.Label(frame_tempo_proximo_ponto, text="Calculando...", bg="#e0f2f7", font=("Arial", 10))
tempo_restante_label.pack(pady=5)
tk.Button(frame_tempo_proximo_ponto, text="Voltar para Menu", command=lambda: mostrar_tela("pos_login"), bg="#ff9800", fg="white").pack(pady=10)

# Tela Cadastro de Usuário
frame_cadastro = tk.Frame(janela, bg="#e0f2f7")
frames["cadastro"] = frame_cadastro
tk.Label(frame_cadastro, text="Novo Usuário:", bg="#e0f2f7").pack()
novo_usuario_entry = tk.Entry(frame_cadastro)
novo_usuario_entry.pack()
tk.Label(frame_cadastro, text="Nova Senha:", bg="#e0f2f7").pack()
nova_senha_entry = tk.Entry(frame_cadastro, show="*")
nova_senha_entry.pack()
tk.Button(frame_cadastro, text="Cadastrar", command=lambda: cadastrar_usuario(novo_usuario_entry.get(), nova_senha_entry.get()), bg="#4caf50", fg="white").pack(pady=10)
tk.Button(frame_cadastro, text="Voltar", command=lambda: mostrar_tela("login"), bg="#ff9800", fg="white").pack(pady=5)

# Tela Cadastro de Empresa
frame_cadastro_empresa = tk.Frame(janela, bg="#e0f2f7")
frames["cadastro_empresa"] = frame_cadastro_empresa
tk.Label(frame_cadastro_empresa, text="Nome da Empresa:", bg="#e0f2f7").pack()
nome_empresa_cadastro_entry = tk.Entry(frame_cadastro_empresa)
nome_empresa_cadastro_entry.pack()
tk.Label(frame_cadastro_empresa, text="CNPJ:", bg="#e0f2f7").pack()
cnpj_empresa_cadastro_entry = tk.Entry(frame_cadastro_empresa)
cnpj_empresa_cadastro_entry.pack()
tk.Label(frame_cadastro_empresa, text="Número de Funcionários:", bg="#e0f2f7").pack()
funcionarios_empresa_cadastro_entry = tk.Entry(frame_cadastro_empresa)
funcionarios_empresa_cadastro_entry.pack()
tk.Label(frame_cadastro_empresa, text="Telefone:", bg="#e0f2f7").pack()
telefone_empresa_cadastro_entry = tk.Entry(frame_cadastro_empresa)
telefone_empresa_cadastro_entry.pack()
tk.Label(frame_cadastro_empresa, text="Endereço:", bg="#e0f2f7").pack()
endereco_empresa_cadastro_entry = tk.Entry(frame_cadastro_empresa)
endereco_empresa_cadastro_entry.pack()
tk.Button(frame_cadastro_empresa, text="Salvar", command=lambda: cadastrar_empresa(
    nome_empresa_cadastro_entry.get(), cnpj_empresa_cadastro_entry.get(),
    funcionarios_empresa_cadastro_entry.get(), telefone_empresa_cadastro_entry.get(),
    endereco_empresa_cadastro_entry.get()), bg="#4caf50", fg="white").pack(pady=10)
tk.Button(frame_cadastro_empresa, text="Voltar", command=lambda: mostrar_tela("login"), bg="#ff9800", fg="white").pack(pady=5)

# Tela de Configurações da Empresa
frame_empresa_config = tk.Frame(janela, bg="#e0f2f7")
frames["empresa_config"] = frame_empresa_config
tk.Label(frame_empresa_config, text="Configurações da Empresa", bg="#e0f2f7", font=("Arial", 16)).pack(pady=10)

horista_var = tk.BooleanVar()
tk.Checkbutton(frame_empresa_config, text="Funcionários são horistas", variable=horista_var, bg="#e0f2f7").pack(anchor=tk.W)

hora_extra_var = tk.BooleanVar()
tk.Checkbutton(frame_empresa_config, text="Permitir hora extra", variable=hora_extra_var, bg="#e0f2f7").pack(anchor=tk.W)

tk.Label(frame_empresa_config, text="Espaço para RH:", bg="#e0f2f7", font=("Arial", 12)).pack(pady=10)
rh_text = tk.Text(frame_empresa_config, height=5, width=30)
rh_text.pack()

tk.Button(frame_empresa_config, text="Salvar Configurações", command=lambda: messagebox.showinfo("Info", "Configurações salvas!"), bg="#4caf50", fg="white").pack(pady=10)
tk.Button(frame_empresa_config, text="Voltar para Login", command=lambda: mostrar_tela("login"), bg="#ff9800", fg="white").pack(pady=5)

janela.mainloop()