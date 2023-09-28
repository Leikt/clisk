from typing import Annotated

import typer

import clisk

clisk.set_up(help='An app to greet everyone!', add_completion=False)
clisk.intermediate('say', help="Say a typical greeting phrase.")


@clisk.command('say', 'hello', help='Say hello to someone.')
def cmd_say_hello(
        name: Annotated[str, typer.Argument(help='The name of the person to greet.')]
):
    print(f'Hello, {name}!')


@clisk.command('say', 'hi', help='Say hi to someone.')
def cmd_say_hi(
        name: Annotated[str, typer.Argument(help='The name of the person to greet.')]
):
    print(f'Hi, {name}')


if __name__ == '__main__':
    clisk.run()
