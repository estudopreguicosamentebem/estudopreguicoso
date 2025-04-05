import streamlit as st
from g4f.client import Client
import time

def formatar_prompt(assuntos):
    """Gera o prompt estruturado para a API."""
    return f"""
    Crie um resumo detalhado em português com base nestes tópicos:
    {assuntos}

    Requisitos:
    - Estruture de forma detalhada e abrangente
    - Use linguagem simples mas formal
    - Seja claro e objetivo
    - Inclua exemplos práticos quando relevante
    - Mantenha a coerência entre os tópicos
    - Utilize formatação Markdown para organização
    - Limite de 1500 palavras

    Estruture da seguinte forma:
    # Título Principal
    ## Subtópicos quando necessário
    - Pontos chave
    - Explicações concisas
    - Dados relevantes
    """

def gerar_resumo(prompt):
    """Envia a solicitação para a API e retorna a resposta."""
    client = Client()
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            web_search=True,
            timeout=30
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
        return None

def main():
    st.set_page_config(page_title="Estudo Preguiçoso", page_icon="📝")
    
    st.title("📝 Estudo Preguiçoso")
    st.markdown("---")
    
    with st.expander("ℹ️ Como usar"):
        st.write("""
        1. Digite os tópicos que deseja resumir (separados por vírgula ou ponto e vírgula)
        2. Clique no botão 'Gerar Resumo'
        3. Aguarde o processamento
        4. Visualize o resultado
        """)
    
    assuntos = st.text_area(
        "Digite os tópicos que deseja resumir:",
        placeholder="Ex: Inteligência Artificial, Machine Learning, Deep Learning"
    )
    
    if st.button("Gerar Resumo", type="primary"):
        if not assuntos.strip():
            st.warning("Por favor, insira pelo menos um tópico para gerar o resumo.")
            return
        
        with st.spinner("⏳ Processando sua solicitação..."):
            inicio = time.time()
            
            prompt = formatar_prompt(assuntos)
            resumo = gerar_resumo(prompt)
            
            if resumo:
                st.success("Resumo gerado com sucesso!")
                st.markdown("---")
                st.subheader("Resultado")
                st.markdown(resumo)
                
                st.markdown("---")
                st.write(f"⏱️ Tempo total: {time.time() - inicio:.2f} segundos")
            else:
                st.error("Não foi possível gerar o resumo.")

if __name__ == "__main__":
    main()
