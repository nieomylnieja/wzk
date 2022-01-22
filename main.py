import click

from click_utils import ImageParamType, rename_kwargs
import lsb
import vis


@click.group()
def cli():
    pass


@click.command("lsb")
@click.option("-x", "--execute", required=True, type=click.Choice(["encode", "decode"], case_sensitive=False))
@click.option("-m", "--message", type=click.STRING, default="test message")
@click.option("-o", "--output", type=click.STRING, default="out.png")
@click.argument("file", type=ImageParamType())
@rename_kwargs(img="file")
def steganography_lsb(execute, output, message, img):
    if execute == "encode":
        lsb.encode(img, message, output)
    if execute == "decode":
        lsb.decode(img)


@click.command("vis")
@click.option("-x", "--execute", required=True, type=click.Choice(["encode", "decode"], case_sensitive=False))
@click.option("-o", "--output", type=click.STRING, default="out.png")
@click.option("-s", "--shares", type=click.STRING, default=("share1.png", "share2.png"), multiple=True)
@click.argument("file", type=ImageParamType(), required=False)
@rename_kwargs(img="file")
def visual_cryptography(execute, output, img, shares):
    if execute == "encode":
        if not img:
            raise click.exceptions.MissingParameter("missing required input file argument")
        vis.encode(img)
    if execute == "decode":
        if not shares or len(shares) != 2:
            raise click.exceptions.MissingParameter("missing required option --shares")
        if len(shares) != 2:
            raise click.exceptions.BadParameter("--shares should have exactly two values")
        vis.decode(*shares, output)


cli.add_command(steganography_lsb)
cli.add_command(visual_cryptography)

if __name__ == '__main__':
    cli()
