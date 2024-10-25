from typing import Optional
import typer

from postman_drf import __app_name__, __version__, PostmanToDjango


app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Show the application's version and exit.",
    callback=_version_callback,
    is_eager=True,
    )
) -> None:
    return


@app.command()
def postman_to_drf(collection_file: str, destination: str, environment_file: str | None = None):
    p2d = PostmanToDjango()
    p2d.postman_to_django(
        collection_file=collection_file,
        destination=destination,
        environment_file=environment_file
    )


@app.command()
def create():
    print("Creating user: Hiro Hamada")


@app.command()
def delete():
    print("Deleting user: Hiro Hamada")


if __name__ == '__main__':
    app()
