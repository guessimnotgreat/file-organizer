import os
import click
from shutil import move
from collections import defaultdict


@click.command()
@click.argument('source', type=click.Path(exists=True), required=False)
@click.argument('destination', type=click.Path(), required=False)
@click.option('--dry-run', is_flag=True, help="Simulate file organization without actually moving files.")
def organize_files(source, destination, dry_run=False):

    if source is None or destination is None:
        click.echo(
            click.style("Please provide source and destination directories as command-line arguments.",
                   fg='red', bold=True)
            )
        return

    dict = _get_file_paths(source)

    for file_type in dict:
            
        for filename in dict[file_type]:
            destination_folder = os.path.join(destination, file_type)
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            
            original_path = os.path.join(source, filename)
            new_path = os.path.join(destination_folder, filename)

            if dry_run:
                _dry_run(destination_folder, filename)
                
                is_confirm = False
                while is_confirm is False: 
                    confirmation = input("Do you want to proceed? (yes/no): ").lower()
                    if confirmation in {'yes', 'y'}:
                        _move_file(original_path, new_path, filename, destination_folder)
                        is_confirm = True
                    elif confirmation in {'no', 'n'}:
                        break
                    else:
                        print(f"Invalid input. Please enter 'yes' or 'no'.")
            else:
                _move_file(original_path, new_path, filename, destination_folder)

            

def _dry_run(destination_folder, filename):
    print(f"{filename} will be move to {destination_folder}")

def _move_file(original_path, new_path, filename, destination_folder):
    try:
        move(original_path, new_path)
        print(f"Moved: {filename} to {destination_folder}")
    except Exception as e:
        print(f"Error moving {filename}: {e}")

def _get_file_paths(source):
    paths = defaultdict(list)
    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        file_type = _get_file_type(file_path, filename)
        if file_type is not None:
            paths[file_type].append(filename)
    return paths

def _get_file_type(file_path, filename):
    return filename.split('.')[-1].lower() if os.path.isfile(file_path) else None


if __name__ == '__main__':
    organize_files()