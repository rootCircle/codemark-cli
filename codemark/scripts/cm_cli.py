import click

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
def list():
    """Lists all assignments"""
    print("Will list all assignment here.")

@click.command()
@click.option('--code', help='Assignment Code')
@click.argument('code')
def get(code):
    """Fetches assignments from cloud based on assignment Code"""
    print("Downloading assignment")

@click.command()
def check():
    """Checks the code against selected test cases and report errors"""
    print("Checks the code based on cached assignment code fetched from a file")


@click.command()
def submit():
    """Submit the code against selected test cases and report errors"""
    print("Checks the code based on cached assignment code fetched from a file")

@click.command()
def review():
    """Let AI review your code and recommend error you might be doing"""
    print("CHATGPT API")

@click.command()
def doctor():
    """Fixes any known common issues for the app"""
    print("Checks init file config and credentials and if server is down. Version etc")

cli.add_command(init)
cli.add_command(list)
cli.add_command(get)
cli.add_command(check)
cli.add_command(submit)
cli.add_command(review)
cli.add_command(review)
