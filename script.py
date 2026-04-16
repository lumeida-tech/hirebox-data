import asyncio
from src.gemma_ai import Gemma_Question_Generator


async def main() -> None:
    question = await Gemma_Question_Generator(
        prompt="Génère une question d'entretien pertinente basée sur le CV fourni."
    ).generate_question("Contenu du CV")
    print("Question générée:", question)


if __name__ == "__main__":
    asyncio.run(main())
