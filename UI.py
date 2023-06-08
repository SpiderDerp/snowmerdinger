import click
from colorama import Fore
from colorama import init as colorama_init
from art import text2art
from tqdm import trange
from time import sleep


colorama_init(autoreset=True)

@click.command()
def makeCLI():
    title = text2art("SNOWMERDINGER", font='medium')
    print(f"{Fore.LIGHTCYAN_EX}{title}")
    click.pause()
    click.clear()
    artl4 = text2art("MENU", font='medium')
    print(f"{Fore.LIGHTCYAN_EX}{artl4}")
    width = click.prompt(
        'Enter the width of the plot in meters ', type=int, default=1)
    height = click.prompt('Enter the height of the plot in meters ', type=int, default=1)
    if width <= 0:
        width = 1
    if height <=0:
        height = 1
    artl5 = "Place your robot at the bottom right corner of the plot and press any key to start"
    print(f"{Fore.LIGHTRED_EX}{artl5}")
    click.pause()
    click.clear()
    return width, height


if __name__ == '__main__':
    makeCLI()