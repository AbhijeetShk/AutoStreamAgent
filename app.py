from graph import build_graph


def main():
    bot = build_graph()
    state = {}
    print('AutoStream Assistant (type quit to exit)')

    while True:
        msg = input('You: ').strip()
        if msg.lower() in ['quit', 'exit']:
            break

        result = bot.invoke({"message": msg, "state": state})
        state = result["state"]
        print('Bot:', result["reply"])


if __name__ == '__main__':
    main()