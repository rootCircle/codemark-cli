import click
import codemark.get
import codemark.review
import codemark.list
import codemark.initialise
import codemark.doctor
import codemark.check
import codemark.logout
import codemark.submit

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
    codemark.initialise.initApp()

@click.command()
@click.option( '-S', '--submitted', is_flag=True, help='Show only completed assignments')
@click.option( '-P', '--pending', is_flag=True, help='Show only pending assignments')
def list(submitted, pending):
    """Lists all assignments"""
    if submitted and pending:
        click.echo("Error: -S and -P are mutually exclusive.")
        return
    codemark.list.listSmart(submitted, pending)


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
    codemark.check.checkCode()

@click.command()
@click.option( '-f', '--force', is_flag=True, help='Submit code even if all tests have not passed')
def submit(force):
    """Submit the code against selected test cases and report errors"""
    codemark.submit.submit(force)

@click.command()
@click.option('--code', help='Assignment Code')
@click.argument('code')
def get(code):
    """Fetches assignments from cloud, based on assignment Code"""
    #TODO: Check if assignment is completed or not and inform users
    codemark.get.fetch(code)

@click.command()
def review():
    """Let AI review your code and recommend error you might be doing"""
    codemark.review.reviewCode()

@click.command()
def doctor():
    """Fixes any known common issues for the app"""
    codemark.doctor.doctor()

@click.command()
def logout():
    """Logout the user"""
    codemark.logout.logout()

cli.add_command(init)
cli.add_command(list)
cli.add_command(get)
cli.add_command(check)
cli.add_command(submit)
cli.add_command(review)
cli.add_command(doctor)
cli.add_command(logout)