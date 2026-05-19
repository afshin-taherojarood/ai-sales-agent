from dotenv import load_dotenv
from agent import Agent

load_dotenv()

agent = Agent()

print("دستیار فروش آماده است! (برای خروج 'خروج' بنویس)\n")

while True:
    user_input = input("شما: ")

    if user_input == "خروج":
        print("خداحافظ!")
        break

    response = agent.chat(user_input)
    print(f"\nدستیار: {response}\n")