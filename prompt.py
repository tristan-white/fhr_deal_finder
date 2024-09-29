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

async def cli():
    session = PromptSession()

    while True:
        try:
            with patch_stdout():
                result = await session.prompt_async("[ None ]> ", )
        except KeyboardInterrupt:
            print_formatted_text(HTML(
                "Press <yellow><b>Ctrl-D</b></yellow> to exit."
            ))
            continue
        except EOFError:
            print("eof error")
            break
        else:
            if result not in cmds:
                help()
            else:
                print("not implemented yet")

if __name__ == "__main__":
    asyncio.run(cli())