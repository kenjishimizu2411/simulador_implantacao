# 🚀 Simulador de Implantação de Software (AI-Driven)

> **Powered by Kenji Shimizu**

Este é um simulador interativo de negociação e implantação de software que utiliza Inteligência Artificial de última geração (**Google Gemini 2.5 Flash**) para treinar analistas em *Soft Skills*, gestão de expectativas e resolução de conflitos com diferentes perfis de clientes.

---

## 🎯 O Problema que Resolvemos

No mundo corporativo, implantações de software frequentemente falham não por erros de código, mas por falhas na comunicação e alinhamento. Este simulador coloca o analista diante de três arquétipos clássicos, cada um com motivações e "dores" reais:

- **Márcia (Diretora de Operações):** Pressão extrema por prazos e urgência operacional. Quer ver o sistema rodando "ontem".
- **Roberto (Gerente Financeiro):** Cético, defensivo e traumatizado por projetos fracassados no passado. Exige transparência e provas.
- **Sérgio (CEO/Fundador):** Brilhante nos negócios, mas com baixo letramento digital. Acredita que o software é uma "varinha mágica".

---

## 🛠️ Stack Tecnológica

- **Linguagem:** Python 3.10+
- **Interface:** [Streamlit](https://streamlit.io/) (Framework Web focado em Ciência de Dados e IA)
- **IA Engine:** [Google GenAI SDK](https://github.com/google-gemini/generative-ai-python) (Modelo Gemini 2.5 Flash)
- **Segurança:** Gestão de chaves via Streamlit Secrets (Conformidade com DevSecOps)

---

## ✨ Funcionalidades Principais

- **Personas Dinâmicas:** Sistema de *System Prompts* estruturados que garantem comportamentos humanos, reativos e consistentes.
- **Gatilhos de Acordo (Semantic Triggers):** Lógica que detecta o fechamento do contrato através de *Tokens de Controle* (`[ACORDO_FECHADO]`) injetados via prompt.
- **Relatório de Desempenho (LLM as a Judge):** Após o sucesso na negociação, um **Mentor de IA** analisa todo o histórico da conversa, fornecendo feedback consultivo e uma nota de 0 a 10.
- **Interface Premium:** Layout responsivo com colunas, uso de popovers para biografias imersivas e avatares personalizados no chat.

---

## 🚀 Como Executar o Projeto

### 1. Clonar o Repositório

```bash
git clone https://github.com/kenjishimizu2411/simulador_implantacao.git
cd simulador_implantacao
```
---

### 2. Configurar o Ambiente Virtual

```bash
python -m venv .venv
```
```bash
# Ativar no Windows:
.\.venv\Scripts\activate
```
```bash
# Ativar no Linux/Mac:
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

---
### 3. Configurar sua API Key
Crie uma pasta .streamlit na raiz do projeto e, dentro dela, um arquivo secrets.toml:

```bash
GOOGLE_API_KEY = "SUA_CHAVE_AQUI"
```

---
### 4. Rodar a Aplicação

```bash
streamlit run src/main.py
```

---

🛡️ Segurança e Resiliência
Proteção de Dados: Arquivo .gitignore configurado para impedir o vazamento acidental de ambientes virtuais (.venv/) e segredos de API (.streamlit/).

Programação Defensiva: Tratamento de exceções e verificação de existência de assets (fotos) para garantir que a aplicação nunca quebre em produção.

Arquitetura Moderna: Uso de injeção de dependência via genai.Client, facilitando a manutenção e futuras atualizações de modelos.

🧪 Dica para Avaliadores (Testing Hook)
Para validar o fluxo de vitória e a geração automática do Relatório de Desempenho sem precisar completar toda a jornada de negociação, utilize a palavra-chave secreta: thresh em qualquer momento da conversa com os clientes.