from graph import build_graph


def main():
    graph = build_graph()
    state = {"messages": []}

    print("AutoStream Assistant (type quit to exit)")

    while True:
        text = input("You: ").strip()
        if text.lower() in ["quit", "exit"]:
            break

        result = graph.invoke({**state, "user_input": text})
        state = result
        print("Bot:", result["reply"])


if __name__ == "__main__":
    main()