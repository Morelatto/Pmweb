from bot import Bot

ACCOUNTS = [["nome_conta1", "login_conta1", "senha_conta1"], ["nome_conta2", "login_conta2", "senha_conta2"]]

ACCOUNT_LIST_2 = []
ACCOUNT_LIST_5 = []
for account in ACCOUNTS:
    if account[3] == "2":
        ACCOUNT_LIST_2.append(account)
    else:
        ACCOUNT_LIST_5.append(account)

if __name__ == "__main__":
    running = False
    for account in ACCOUNT_LIST_5:
        bot = Bot(account[1], account[2], account[0].replace(" ", "_"), "5", running)
        running = True
        bot.log_in()
        bot.login_code()
        user_success = bot.attempt_creation_user()

        if user_success:
            bot.fill_fields()
            bot.create_user()
        bot.logout()
