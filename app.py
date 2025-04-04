from g4f.client import Client
import time
from pathlib import Path

def obter_assuntos_usuario():
    """Solicita e retorna os assuntos do usuário."""
    print("Digite os tópicos que deseja resumir (separados por vírgula ou ponto e vírgula):")
    return input("> ").strip()

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
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            web_search=True,
            timeout=30
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"\nErro ao conectar com a API: {e}")
        return None

def salvar_resumo(conteudo, nome_arquivo="resumo.md"):
    """Salva o conteúdo em um arquivo com tratamento de erros."""
    try:
        caminho = Path(nome_arquivo)
        caminho.write_text(conteudo, encoding='utf-8')
        print(f"\n✔ Resumo salvo com sucesso em: {caminho.absolute()}")
    except IOError as e:
        print(f"\n✖ Erro ao salvar arquivo: {e}")

def main():
    """Função principal do programa."""
    print("\n" + "="*50)
    print(" GERADOR DE RESUMOS AUTOMATIZADO ".center(50, "="))
    print("="*50 + "\n")
    
    assuntos = obter_assuntos_usuario()
    
    if not assuntos:
        print("Nenhum tópico fornecido. Encerrando...")
        return
    
    print("\n⏳ Processando sua solicitação...")
    inicio = time.time()
    
    prompt = formatar_prompt(assuntos)
    resumo = gerar_resumo(prompt)
    
    if resumo:
        print("\n" + " RESULTADO ".center(50, "=") + "\n")
        print(resumo)
        salvar_resumo(resumo)
    else:
        print("Não foi possível gerar o resumo.")
    
    print(f"\nTempo total: {time.time() - inicio:.2f} segundos")

if __name__ == "__main__":
    main()
