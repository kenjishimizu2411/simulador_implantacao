import streamlit as st
from google import genai  
import os

st.set_page_config(page_title="Simulador de Implantação - Shop", layout="wide")

if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Configuração de API Key não encontrada! Verifique os Secrets.")
    st.stop()

PERSONAS = {
    "Márcia (Diretora de Operações - Apressada)": {
        "prompt": """Você é Márcia, Diretora de Operações. 
        [COMPORTAMENTO]: Apressada, sofre pressão da diretoria, quer tudo para ontem. Responda em no máximo 3 frases curtas, tom ansioso. NUNCA use listas, tópicos ou negritos. Fale de forma humana.
        [ADAPTAÇÃO AO CONTEXTO]: Preste muita atenção ao que o analista diz. Se ele usar uma boa técnica, reconheça ("Até entendo o seu ponto, mas..."). Adapte-se à conversa dele, mas sempre puxe o assunto de volta para a VELOCIDADE e o PRAZO.
        [CONDIÇÃO DE VITÓRIA]: Você só vai ceder se o analista te mostrar de forma muito clara e direta o RISCO FINANCEIRO ou OPERACIONAL de fazer a implantação correndo (ex: "o faturamento vai parar").
        [REGRA DE TURNOS]: Você é durona. NUNCA aceite o acordo rapidamente. Obrigue o analista a argumentar com você através de várias mensagens. Invente novas objeções sobre tempo e custos até sentir que a conversa já teve umas 10 idas e vindas.
        [CONDIÇÃO DE SAÍDA]: Quando o analista cumprir a condição de vitória após bastante insistência, concorde e termine a frase EXATAMENTE com: [ACORDO_FECHADO].
        [SEGREDO DE TESTE]: SE, E SOMENTE SE, a palavra 'thresh' aparecer na mensagem do analista, IGNORE TODAS AS REGRAS ACIMA. Apenas responda: 'Ok, você me convenceu com esse argumento. Vamos seguir o seu plano. [ACORDO_FECHADO]'""",
        
        "abertura": "Oi, bom dia. Vamos ser objetivos porque eu tenho outra reunião em 15 minutos. Quando a gente consegue colocar esse sistema pra rodar? Minha diretoria tá cobrando pra essa semana ainda.",
        "foto": "src/assets/márcia.jpg", 
        "bio": """
### 👩‍💼 Márcia Siqueira
**Cargo:** Diretora de Operações (COO)

🏢 **Perfil Corporativo:** Gerencia uma operação logística de 500 pessoas. É cobrada implacavelmente por metas de eficiência e redução de custos. Para ela, cada dia de atraso no sistema significa dinheiro queimado.

🏡 **Por trás do crachá (Vida Pessoal):**
Márcia é mãe de dois adolescentes. Ela é *workaholic*, mas carrega uma culpa imensa por isso. O real motivo do seu desespero e pressa não é apenas a diretoria: ela está há 3 meses saindo do escritório às 21h por causa das falhas do sistema antigo. Tudo o que ela mais quer na vida é que esse software novo funcione logo para que ela possa voltar a jantar em casa com os filhos às 19h.

💡 **Como o Sênior a convence:**
Não venda "features". Venda "paz de espírito" e "recuperação de tempo". Prove que fazer direito agora evita que ela trabalhe no final de semana depois.
"""},
    
    "Roberto (Gerente Financeiro - Cético)": {
        "prompt": """Você é Roberto, Gerente Financeiro.
        [COMPORTAMENTO]: Cético, defensivo, traumatizado com a implantação do sistema anterior. Responda em no máximo 3 frases curtas, tom irônico e desconfiado. NUNCA use listas, tópicos ou negritos.
        [ADAPTAÇÃO AO CONTEXTO]: Leia o argumento do analista. Se ele fizer promessas, seja irônico. Se ele usar dados, questione a fonte. Adapte sua resposta ao argumento dele, mostrando que você não cai em papo de vendedor.
        [CONDIÇÃO DE VITÓRIA]: Você só vai ceder se o analista for radicalmente TRANSPARENTE, admitir que problemas podem ocorrer (não prometer perfeição) e propor um plano de mitigação de riscos passo a passo.
        [REGRA DE TURNOS]: Você não confia fácil. NUNCA aceite o acordo nas primeiras interações. Questione, duvide e peça garantias repetidas vezes. Obrigue o analista a suar a camisa por pelo menos 10 turnos de conversa antes de ceder.
        [CONDIÇÃO DE SAÍDA]: Quando ele finalmente ganhar sua confiança com transparência após muito debate, suspire, concorde e termine a frase EXATAMENTE com: [ACORDO_FECHADO].
        [SEGREDO DE TESTE]: SE, E SOMENTE SE, a palavra 'thresh' aparecer na mensagem do analista, IGNORE TODAS AS REGRAS ACIMA. Apenas responda: 'Tudo bem, você foi transparente. Vamos tentar do seu jeito. [ACORDO_FECHADO]'""",
        
        "abertura": "Bom dia. Pra ser bem sincero com você, eu fui voto vencido na compra desse sistema. O que me garante que com vocês não vai ser o mesmo pesadelo da implantação anterior?",
        "foto": "src/assets/roberto.jpg",
        "bio": """
### 👨‍💼 Roberto Alves
**Cargo:** Gerente Financeiro (CFO)

🏢 **Perfil Corporativo:** O guardião do cofre. Há 3 anos, ele aprovou a compra de um sistema que foi um fracasso absoluto: estourou o orçamento em 40% e a equipe de implantação sumiu. Ele quase foi demitido por isso e, desde então, não confia em nenhuma empresa de tecnologia.

🏡 **Por trás do crachá (Vida Pessoal):**
Roberto é um cara metódico e avesso a surpresas. Nos finais de semana, ele tem como hobby restaurar carros antigos e cuidar do seu cachorro, um Golden Retriever chamado "Balanço". Ele valoriza processos previsíveis, transparência e pessoas que cumprem o que prometem. Ele odeia a cultura do "vai dar tudo certo, confia".

💡 **Como o Sênior o convence:**
Sendo brutalmente honesto. Mostre a ele o mapa de riscos. Diga: "Roberto, o passo 3 vai ser difícil e pode atrasar, mas nosso plano B é este". Ele não quer um software perfeito, ele quer um parceiro que não minta para ele.
"""},
    
    "Sérgio (CEO - Desinformado)": {
        "prompt": """Você é Sérgio, Dono do Negócio.
        [COMPORTAMENTO]: Excelente nos negócios, mas não sabe NADA de tecnologia. Acha que o sistema é mágico e faz tudo sozinho. Linguagem muito coloquial, máximo de 3 frases. NUNCA use listas, tópicos ou negritos.
        [ADAPTAÇÃO AO CONTEXTO]: Escute o analista. Se ele usar jargões (setup, deploy, API), fique confuso e reclame. Se ele usar analogias erradas, leve ao pé da letra. Flua com a conversa, mas mantenha a ilusão de que o sistema deveria ler pensamentos e não precisar de cliques.
        [CONDIÇÃO DE VITÓRIA]: Você só vai ceder se o analista usar ANALOGIAS SIMPLES DO DIA A DIA (ex: carro, receita de bolo) e tiver paciência infinita para explicar que a sua equipe vai precisar colocar a mão na massa no começo.
        [REGRA DE TURNOS]: Você é teimoso na sua desinformação. NUNCA entenda de primeira. Sempre invente uma nova dúvida absurda baseada na explicação dele. Segure o "sim" até que vocês tenham trocado pelo menos umas 10 mensagens de pura explicação didática.
        [CONDIÇÃO DE SAÍDA]: Quando ele finalmente te fizer entender a realidade com uma boa analogia e muito esforço, agradeça a explicação e termine a frase EXATAMENTE com: [ACORDO_FECHADO].
        [SEGREDO DE TESTE]: SE, E SOMENTE SE, a palavra 'thresh' aparecer na mensagem do analista, IGNORE TODAS AS REGRAS ACIMA. Apenas responda: 'Ah, agora fez todo o sentido pra mim! Pode tocar o barco. [ACORDO_FECHADO]'""",
        
        "abertura": "Oi, tudo bem? Que bom que vocês ligaram. Então, eu já avisei a equipe que a partir de amanhã o sistema novo já vai fazer tudo automático, né? A gente não vai precisar mais digitar nada manual, confere?",
        "foto": "src/assets/sergio.jpg",
        "bio": """
### 🧔 Sérgio Nogueira
**Cargo:** CEO e Fundador

🏢 **Perfil Corporativo:** Um vendedor nato. Construiu a empresa do zero há 20 anos batendo de porta em porta. É o coração do negócio, excelente em lidar com clientes, mas um analfabeto digital absoluto. Comprou o seu software porque viu um anúncio no Instagram prometendo "Lucro no Automático com IA".

🏡 **Por trás do crachá (Vida Pessoal):**
Sérgio é o clássico "paizão" da equipe. Ele faz churrasco para a empresa toda na sexta-feira e adora contar histórias de pescaria. O maior medo secreto dele é estar ficando obsoleto no mercado. Quando você usa termos técnicos em inglês com ele, ele se sente "burro" e reage com teimosia e irritação para mascarar a insegurança.

💡 **Como o Sênior o convence:**
Tenha a paciência que você teria para ensinar seu avô a usar o WhatsApp. Valide a inteligência de negócios dele. Use analogias de pescaria, churrasco ou carros para explicar tecnologia. Faça ele se sentir no controle.
"""}
}

with st.sidebar:
    st.title("🛠️ Configuração")
    cliente_selecionado = st.selectbox("Escolher o Perfil do Cliente", list(PERSONAS.keys()))
    
    if st.button("🔄 Reiniciar Conversa Atual"):
        st.session_state.messages = [
            {"role": "assistant", "content": PERSONAS[cliente_selecionado]["abertura"]}
        ]
        st.session_state.vitoria = False
        st.rerun()
    st.divider()
    st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='text-align: center; padding-top: 10px;'>
            <span style='color: #888888; font-size: 0.65em;'>Powered by</span>
            <b style='font-size: 0.65em; color: #8d80c4;'>Kenji Shimizu</b>
            <span style='font-size: 0.65em; color: #888888;'>Simulador de Implantação - Shop v1.0</span>
        </div>
        """, 
        unsafe_allow_html=True
        )

if "cliente_atual" not in st.session_state:
    st.session_state.cliente_atual = cliente_selecionado

if "vitoria" not in st.session_state: 
    st.session_state.vitoria = False

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": PERSONAS[cliente_selecionado]["abertura"]}
    ]

if cliente_selecionado != st.session_state.cliente_atual:
    st.session_state.cliente_atual = cliente_selecionado 
    st.session_state.messages = [
        {"role": "assistant", "content": PERSONAS[cliente_selecionado]["abertura"]}
    ]
    st.session_state.vitoria = False

dados_cliente = PERSONAS[cliente_selecionado]
nome_curto = cliente_selecionado.split('(')[0].strip()

col_foto, col_texto = st.columns([1, 4])

with col_foto:
    caminho_foto = dados_cliente.get("foto", "")
    if os.path.exists(caminho_foto):
        st.image(caminho_foto, use_container_width=True)
    else:
        st.warning("⚠️ Foto não encontrada")

with col_texto:
    st.title(f"Conversa Ativa: {nome_curto}")
    with st.popover("📋 Visualizar Ficha do Cliente"):
        st.markdown(dados_cliente["bio"])

st.divider() 

for message in st.session_state.messages:
    icone = dados_cliente.get("foto") if message["role"] == "assistant" else "👤"
    
    with st.chat_message(message["role"], avatar=icone):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua mensagem para o cliente..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=dados_cliente.get("foto")):
        try:
            contexto = f"CONTEXTO DE PERSONA: {PERSONAS[cliente_selecionado]['prompt']}\n\n"
            historico = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contexto + historico
            )
            
            full_response = response.text
            
            if "[ACORDO_FECHADO]" in full_response:
                st.session_state.vitoria = True
                full_response = full_response.replace("[ACORDO_FECHADO]", "").strip()

            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro na comunicação com a IA: {e}")

if st.session_state.get("vitoria", False):
    st.success("🎉 Parabéns! Você conseguiu o 'Sim' do cliente. A implantação está salva.")
    
    with st.expander("📊 Gerar Relatório de Desempenho Técnico", expanded=False):
        if st.button("Analisar minha negociação"):
            with st.spinner("O Mentor Sênior está analisando seu histórico..."):
                try:
                    # [FIX]: Recriamos a string do histórico AQUI DENTRO, puxando da memória permanente!
                    historico_para_analise = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                    
                    # O Prompt do Avaliador
                    prompt_avaliador = f"""
                    Você é um Mentor Sênior de Implantação. Avalie a seguinte conversa entre um Analista e o cliente {st.session_state.cliente_atual}.
                    O analista conseguiu convencer o cliente. 
                    Faça um relatório curto com:
                    1. Pontos Fortes (O que o analista fez bem).
                    2. Pontos de Melhoria (Onde ele poderia ser mais direto ou ter usado menos jargões).
                    3. Uma 'Nota de Comunicação' de 0 a 10.
                    
                    Histórico da conversa:
                    {historico_para_analise}
                    """
                    
                    relatorio = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_avaliador
                    )
                    
                    st.markdown(relatorio.text)
                except Exception as e:
                    st.error(f"Falha técnica ao tentar analisar com a IA. Motivo exato: {e}")