import click
import codemark.get
import codemark.review

@click.group()
def cli():
    """A command-line interface that helps you manage your coding assignments and tests with the CodeMark cloud service.
     
     With this tool, you can easily initialize the configuration, list assignments, fetch and check your code,
     submit your code for grading, and get AI-powered error recommendations.
     
     The tool is designed to simplify your experience with CodeMark and streamline your coding workflow."""
    pass

@click.command()
def init():
    """Initialize the configuration globally for codemark"""
    print("ASK user for EMAIL AND API KEY")
    print("Store the .conf file inside home directory")

@click.command()
@click.option( '-C', '--completed', is_flag=True, help='Show only completed assignments')
@click.option( '-P', '--pending', is_flag=True, help='Show only pending assignments')
def list(completed, pending):
    """Lists all assignments"""
    if completed and pending:
        click.echo("Error: -C and -P are mutually exclusive.")
        return
    if completed:
        click.echo("Will list only completed assignments")
    elif pending:
        click.echo("Will list only pending assignments")
    else:
        click.echo("Will list all assignments")


@click.command()
@click.option('--code', help='Assignment Code')
@click.argument('code')
def get(code):
    """Fetches assignments from cloud, based on assignment Code"""
    #TODO: Check if assignment is completed or not and inform users
    codemark.get.fetch(code)


@click.command()
def check():
    """Checks the code against selected test cases and report errors"""
    print("Checks the code based on cached assignment code fetched from a file")


@click.command()
@click.option( '-f', '--force', is_flag=True, help='Submit code even if all tests have not passed')
def submit(force):
    """Submit the code against selected test cases and report errors"""
    if force:
        print("Forced!")
    print("Checks the code based on cached assignment code fetched from a file. Submit late")

@click.command()
def review():
    """Let AI review your code and recommend error you might be doing"""
    codemark.review.reviewCode()

@click.command()
def doctor():
    """Fixes any known common issues for the app"""
    print("Checks init file config and credentials and if server is down. Version, compilers etc")

cli.add_command(init)
cli.add_command(list)
cli.add_command(get)
cli.add_command(check)
cli.add_command(submit)
cli.add_command(review)
cli.add_command(doctor)
