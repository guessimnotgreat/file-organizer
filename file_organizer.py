import os
import click
from shutil import move
from collections import defaultdict
import logging
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='file_organizer.log',
    filemode='a'
)

class MessageType(Enum):
    DEFAULT = "default"
    ECHO_INFO = "echo_info"
    ECHO_ERROR = "echo_error"

def _log_and_print(message, level=logging.INFO, message_type=MessageType.DEFAULT):
    logging.log(level, message)
    
    if message_type == MessageType.DEFAULT:
        click.echo(message)
    elif message_type == MessageType.ECHO_INFO:
        click.echo(click.style(message, fg='green', bold=True))
    elif message_type == MessageType.ECHO_ERROR:
        click.echo(click.style(message, fg='red', bold=True))

@click.command()
@click.argument('source', type=click.Path(exists=True), required=False)
@click.argument('destination', type=click.Path(), required=False)
@click.option('--dry-run', is_flag=True, help="Simulate file organization without actually moving files.")
def organize_files(source, destination, dry_run=False):

    _log_and_print("===== STARTING FILE ORGANIZER =====")

    if source is None or destination is None:
        _log_and_print("Please provide source and destination directories as command-line arguments.", message_type=MessageType.ECHO_ERROR)
        return

    file_dict = _get_file_paths(source)

    for file_type in file_dict:
            
        to_move_list = []
        for filename in file_dict[file_type]:
            destination_folder = os.path.join(destination, file_type)

            original_path = os.path.join(source, filename)
            new_path = os.path.join(destination_folder, filename)

            to_move_list.append([original_path, new_path, filename, destination_folder])
        
        if dry_run:
            _print_dry_run_results(to_move_list)
            is_confirm = False
            while is_confirm is False: 
                confirmation = input("Do you want to proceed? (yes/no): ").lower()
                if confirmation in {'yes', 'y'}:
                    _process_files(to_move_list)
                    is_confirm = True
                elif confirmation in {'no', 'n'}:
                    break
                else:
                    _log_and_print(f"Invalid input. Please enter 'yes' or 'no'.")
        else:
            _process_files(to_move_list)
    
    _log_and_print("===== EXITING PROGRAM =====")

            

def _print_dry_run_results(to_move_list):
    for i in range(len(to_move_list)):
        destination_folder, filename = to_move_list[i][-1], to_move_list[i][-2]
        _log_and_print(f"{filename} will be moved to {destination_folder}", message_type=MessageType.ECHO_INFO)

def _process_files(to_move_list):
    # Check and create the destination folder if it doesn't exist
    if to_move_list:
        destination_folder = to_move_list[0][-1]
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

    for i in range(len(to_move_list)):
        original_path, new_path, filename, destination_folder = to_move_list[i]
        try:
            move(original_path, new_path)
            _log_and_print(f"Moved: {filename} to {destination_folder}")
        except Exception as e:
            _log_and_print(f"Error moving {filename}: {e}")

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