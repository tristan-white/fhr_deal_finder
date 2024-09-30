from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit import PromptSession
from prompt_toolkit import Application
from prompt_toolkit.patch_stdout import patch_stdout
import asyncio

cmds = [
    "help",
]

def help():
    print("Available commands:")
    for cmd in cmds:
        print_formatted_text(HTML(
            f"\t<b>{cmd}</b>"
        ))

async def main():
    session = PromptSession()

    text = "<mytag fg='skyblue' bg='green'>FHR Deal Finder 0.1.0</mytag>"
    print_formatted_text(HTML(text))

    while True:
        try:
            with patch_stdout():
                result = await session.prompt_async("$ ", )
        except KeyboardInterrupt:
            print_formatted_text(HTML(
                "Press <yellow><b>Ctrl-D</b></yellow> to exit."
            ))
            continue
        except EOFError:
            print("Exiting...")
            break
        else:
            if result not in cmds:
                help()
            else:
                print("not implemented yet")

if __name__ == "__main__":
    asyncio.run(main())