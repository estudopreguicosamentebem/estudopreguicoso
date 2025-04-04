from g4f.client import Client

user = input("Quais são os assuntos?")
bullet_points = user

prompt = f"""Crie um resumo detalhado em português com base nestes tópicos:
{bullet_points}

Estruture da seguinte forma:
- Introdução sobre a transição histórica
- Análise de cada processo de centralização por país
- Explicação do Mercantilismo como sistema econômico
- Conclusão sobre a importância do período"""

client = Client()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    web_search=False
)

respo = response.choices[0].message.content
print(respo)  # Optional: Display the response in the console

with open("resumo.txt", "w", encoding="utf-8") as file:
    file.write(respo)

print("\nResumo salvo em 'resumo.txt'!")
