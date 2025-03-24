import tkinter as tk
from tkinter import messagebox
import random

# Função para gerar dados fictícios das máquinas
def gerar_dados():
    dados = {}
    for maquina in ["M1", "M2", "M3"]:
        # Gera valores normais na maioria das vezes
        if random.random() < 0.9:  # 90% de chance de valores normais
            temperatura = random.randint(50, 90)
            velocidade = random.randint(10, 100)
            defeitos = random.randint(0, 5)
        else:  # 10% de chance de valores fora dos parâmetros
            temperatura = random.choice([random.randint(40, 49), random.randint(91, 100)])
            velocidade = random.choice([random.randint(5, 9), random.randint(101, 120)])
            defeitos = random.randint(6, 10)

        dados[maquina] = {
            "temperatura": temperatura,
            "velocidade": velocidade,
            "defeitos": defeitos
        }
    return dados

# Função para verificar os parâmetros
def verificar_parametros(dados):
    alertas = []
    maquinas_fora = 0

    for maquina, valores in dados.items():
        if not (50 <= valores["temperatura"] <= 90):
            alertas.append(f"{maquina} - Temperatura fora do ideal: {valores['temperatura']}°C")
            maquinas_fora += 1
        if not (10 <= valores["velocidade"] <= 100):
            alertas.append(f"{maquina} - Velocidade fora do ideal: {valores['velocidade']} u/min")
            maquinas_fora += 1
        if valores["defeitos"] >= 5:
            alertas.append(f"{maquina} - Taxa de defeitos alta: {valores['defeitos']}%")
            maquinas_fora += 1

    if maquinas_fora >= 2:
        alertas.append("Parada de Emergência: Duas ou mais máquinas fora dos parâmetros!")
        messagebox.showerror("Parada de Emergência", "A produção foi parada devido a múltiplos problemas.")

    return alertas

# Função para atualizar o painel
def atualizar_painel():
    dados = gerar_dados()
    alertas = verificar_parametros(dados)

    # Atualiza os dados na interface
    for maquina, valores in dados.items():
        labels[maquina]["temperatura"].config(text=f"Temperatura: {valores['temperatura']}°C")
        labels[maquina]["velocidade"].config(text=f"Velocidade: {valores['velocidade']} u/min")
        labels[maquina]["defeitos"].config(text=f"Defeitos: {valores['defeitos']}%")

    # Atualiza os alertas
    alertas_texto.set("\n".join(alertas) if alertas else "Produção normal")

    # Agenda a próxima atualização
    janela.after(5000, atualizar_painel)  # Atualiza a cada 5 segundos (para teste)

# Interface gráfica
janela = tk.Tk()
janela.title("Painel de Monitoramento - Indústria 4.0")

# Labels para exibir os dados
labels = {}
for i, maquina in enumerate(["M1", "M2", "M3"]):
    frame = tk.Frame(janela, borderwidth=2, relief="solid")
    frame.grid(row=0, column=i, padx=10, pady=10)
    tk.Label(frame, text=f"Máquina {maquina}", font=("Arial", 14)).pack()
    labels[maquina] = {
        "temperatura": tk.Label(frame, text="Temperatura: --°C"),
        "velocidade": tk.Label(frame, text="Velocidade: -- u/min"),
        "defeitos": tk.Label(frame, text="Defeitos: --%")
    }
    for label in labels[maquina].values():
        label.pack()

# Área de alertas
alertas_texto = tk.StringVar()
alertas_texto.set("Produção normal")
tk.Label(janela, text="Alertas:", font=("Arial", 14)).grid(row=1, column=0, columnspan=3)
tk.Label(janela, textvariable=alertas_texto, fg="red").grid(row=2, column=0, columnspan=3)

# Inicia a atualização do painel
atualizar_painel()

janela.mainloop()