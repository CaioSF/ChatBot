import json
from difflib import get_close_matches

def load_conhecimentos(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_conhecimentos(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data,file, indent=2)

def achar_melhor_resposta(user_question:str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_questions(question: str, conhecimentos:dict) -> str | None:
    for q in conhecimentos["questions"]:
        if q["Pergunta"] == question:
            return q["Resposta"]
        


def chat_bot():
    conhecimentos: dict = load_conhecimentos('conhecimentos.json')
    print("Bem vindo ao atendimento virtual FriCarnes Filho")

    while True:
        user_input: str = input('Você: ')

        if user_input.lower() == 'quit':
            print("LEMBRANDO! você estava conversando com um atendente virtual!")
            break

        best_match: str | None = achar_melhor_resposta(user_input, [q["Pergunta"] for q in conhecimentos["questions"]])

        if best_match:
            answer: str = get_answer_for_questions(best_match, conhecimentos)
            print(f'Bot: {answer}')
        else:

            print(f'Bot: Eu não tenho resposta pra essa pergunta. Você pode me ensinar?')
            new_answer: str = input('Digite a resposta ou escreva "pular" para fazer outra pergunta: ')

            if new_answer.lower() != 'pular':
                conhecimentos['questions'].append({"Pergunta": user_input, "Resposta": new_answer})
                save_conhecimentos('conhecimentos.json', conhecimentos)
                print('Bot: Obrigado! Eu aprendi uma nova resposta!')


if __name__ == '__main__':
    chat_bot()


