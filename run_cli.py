from cohost.generator import generate_cohost_response

def main():
    print("Generative Podcast Co-Host (Free API) — type 'exit' to quit\n")
    while True:
        user_in = input("You: ")
        if user_in.lower() in ("exit", "quit"):
            break
        reply = generate_cohost_response(f"Podcast Co-Host, reply conversationally to: {user_in}")
        print("Co-Host:", reply)

if __name__ == "__main__":
    main()
