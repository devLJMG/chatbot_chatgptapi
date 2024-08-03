#developed by Luciano
# Date 02/01/2023

from tkinter import *
from tkinter import ttk
import pyttsx3
import openai  # Supondo que você está usando a API OpenAI

openai.api_key = 'insira_usa_api'  # Substitua 'YOUR_API_KEY' pela sua chave de API real

# Configuração e inicialização da sintetização de fala TTS
tts_engine = pyttsx3.init()

# Função para chamar a API e obter uma resposta
def gerar_resposta(pergunta):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente útil."},
                {"role": "user", "content": pergunta}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"

# Função para narrar texto usando pyttsx3
def narrar_texto(texto):
    tts_engine.say(texto)
    tts_engine.runAndWait()

def responder():
    pergunta = entrada.get()
    if not pergunta.strip():
        return

    respostas.append("Você: " + pergunta)

    # Gera uma resposta
    resposta = gerar_resposta(pergunta)
    respostas.append("IA: " + resposta)

    # Adiciona a pergunta na lista lateral
    lista_lateral.insert(END, pergunta)

    # Limpa o conteúdo onde exibe a pergunta e a resposta
    exibePerguntasResposta.delete(1.0, END)

    for resposta in respostas:
        exibePerguntasResposta.insert(END, resposta + "\n\n")

    # Limpa a entrada de texto
    entrada.delete(0, END)

    # Narra a resposta
    narrar_texto(resposta)

# Janela principal
janela = Tk()
janela.title("Chatbot Projeto")
janela.configure(bg="#1c2331")

# Cria uma lista de respostas
respostas = []

# Cria um Frame para a área de exibição de perguntas e respostas com rolagem
frame_exibe = Frame(janela, bg="#1c2331")
frame_exibe.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

scrollbar_text = Scrollbar(frame_exibe)
scrollbar_text.pack(side=RIGHT, fill=Y)

exibePerguntasResposta = Text(frame_exibe, height=20, width=50, bg="#1c2331", fg="#F5F5F5", font=("Arial", 14), yscrollcommand=scrollbar_text.set)
exibePerguntasResposta.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar_text.config(command=exibePerguntasResposta.yview)

# Cria um Frame para a lista lateral com rolagem
frame_lista = Frame(janela, bg="#1c2331")
frame_lista.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="NSEW")

scrollbar_list = Scrollbar(frame_lista)
scrollbar_list.pack(side=RIGHT, fill=Y)

lista_lateral = Listbox(frame_lista, bg="#1c2331", fg="#F5F5F5", yscrollcommand=scrollbar_list.set)
lista_lateral.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar_list.config(command=lista_lateral.yview)

# Configura onde a linha da janela começa
janela.columnconfigure(0, weight=1)
janela.rowconfigure(0, weight=1)

label = Label(janela, text="Pergunta", bg="#1c2331", fg="#F9F9F9")
label.grid(row=1, column=0, pady=10, sticky="W")

entrada = Entry(janela, bg="#1c2331", fg="#F9F9F9", font=("Arial", 18))
entrada.grid(row=2, column=0, pady=10, sticky="NSEW")

botao = Button(janela, text="Perguntar", command=responder, bg="#F9F9F9", font=("Arial", 18))
botao.grid(row=3, column=0, pady=10, sticky="NSEW")

# Maximiza a janela
janela.state("zoomed")
janela.mainloop()
