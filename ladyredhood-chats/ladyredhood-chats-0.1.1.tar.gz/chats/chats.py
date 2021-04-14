from chat_downloader import ChatDownloader
import click


@click.command()
@click.option("--id", default="tvjxnPexKgU", help="The id of the video")
def get_chats(id):
    url = f"https://www.youtube.com/watch?v={id}"
    print(url)
    chat = ChatDownloader().get_chat(url)
    timestamps = []
    buffer = ""
    for m in chat:
        # print(chat.format(m))
        if "!timestamp" in m["message"]:
            timestamps.append(m)
            # print(chat.format(m))
    for m in timestamps:
        buffer = buffer + chat.format(m) + "\n"

    # Return the response in json format
    print(buffer)


if __name__ == '__main__':
    get_chats()