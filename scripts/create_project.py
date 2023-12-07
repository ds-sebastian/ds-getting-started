import json
import os
import pathlib
import shutil
import subprocess
from typing import Optional

CONFIG_FILE = pathlib.Path(__file__).parent.resolve() / "config.json"
COOKIECUTTER_TEMPLATE_PATH = "cookiecutter-template"
DEFAULT_PYTHON_VERSION = "3.11"


class ConfigManager:
    def __init__(self, config_file: pathlib.Path):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> dict:
        if self.config_file.exists():
            with open(self.config_file, "r") as file:
                return json.load(file)
        return {}

    def get(self, key: str, default=None) -> Optional[str]:
        return self.config.get(key, default)

    def set(self, key: str, value: str):
        self.config[key] = value
        with open(self.config_file, "w") as file:
            json.dump(self.config, file)


# ANSI escape codes for colored output
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_colored(message, color):
    print(f"{color}{message}{Colors.ENDC}")


def install_dependencies():
    # Check if cookiecutter is installed via pipx
    if not shutil.which("cookiecutter"):
        print_colored("Installing Cookiecutter...", Colors.OKBLUE)
        subprocess.run(["pip", "install", "cookiecutter"], check=True)


def get_or_set_default_repo_folder(config_manager: ConfigManager):
    default_repo_folder = config_manager.get("default_repo_folder")
    if default_repo_folder:
        return os.path.expanduser(default_repo_folder)

    print_colored("Enter the path for the default projects folder:", Colors.OKGREEN)
    default_repo_folder = input("> ").strip()
    default_repo_folder = os.path.expanduser(default_repo_folder)

    config_manager.set("default_repo_folder", default_repo_folder)
    return default_repo_folder


def get_author_name(config_manager: ConfigManager):
    author_name = config_manager.get("author_name")
    if author_name:
        return author_name

    author_name = input("Enter your name (or your organization/company/team): ")
    config_manager.set("author_name", author_name)
    return author_name


def create_project_with_cookiecutter(
    template_path, default_repo_folder, config_manager: ConfigManager
):
    expanded_repo_folder = os.path.expanduser(default_repo_folder)
    if not os.path.exists(expanded_repo_folder):
        print_colored(
            f"Error: The directory {expanded_repo_folder} does not exist.", Colors.FAIL
        )
        return

    os.chdir(expanded_repo_folder)
    author_name = get_author_name(config_manager)
    project_name = input("Enter the name for the new project: ")
    repo_name = input("Enter the name for the new repository: ")

    full_project_path = pathlib.Path(expanded_repo_folder) / repo_name
    print_colored(f"The project will be created at: {full_project_path}", Colors.OKCYAN)

    confirmation = input("Do you want to continue? [Y/n]: ").strip().lower() or "y"
    if confirmation != "y":
        print_colored("Project creation cancelled.", Colors.WARNING)
        return

    os.chdir(expanded_repo_folder)
    author_name = get_author_name(config_manager)
    project_name = input("Enter the name for the new project: ")
    repo_name = input("Enter the name for the new repository: ")
    module_name = input("Enter the name for the new module: ")
    description = input("Enter a short description of the project: ")
    python_version = (
        input(f"Enter the Python version to use ({DEFAULT_PYTHON_VERSION}): ")
        or DEFAULT_PYTHON_VERSION
    )

    subprocess.run(
        [
            "cookiecutter",
            "--no-input",
            template_path,
            f"repo_name={repo_name}",
            f"project_name={project_name}",
            f"module_name={module_name}",
            f"author_name={author_name}",
            f"description={description}",
            f"python_version={python_version}",
        ],
        check=True,
    )
    return repo_name


def initialize_git(project_path):
    if not shutil.which("git"):
        print_colored(
            "Git is not available. Skipping Git initialization.", Colors.WARNING
        )
        return

    git_init = input("Initialize a Git repository? [Y/n]: ").strip().lower() or "y"
    if git_init == "y":
        try:
            print_colored("Initializing Git repository...", Colors.OKCYAN)
            subprocess.run(
                ["git", "init", "--initial-branch=main"], cwd=project_path, check=True
            )
            subprocess.run(["git", "add", "."], cwd=project_path, check=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"], cwd=project_path, check=True
            )
        except subprocess.CalledProcessError:
            print_colored("Failed to initialize Git repository.", Colors.FAIL)

    # TODO: Add remote bitbucket repo using config file


def setup_conda_environment(repo_name):
    if not shutil.which("conda"):
        print_colored(
            "Conda is not available. Skipping Conda environment setup.", Colors.WARNING
        )
        return

    setup_conda = (
        input("Set up a Conda environment for this project? [Y/n]: ").strip().lower()
        or "y"
    )
    if setup_conda == "y":
        try:
            env_name = repo_name.replace(" ", "_")
            subprocess.run(
                [
                    "conda",
                    "create",
                    "--name",
                    env_name,
                    f"python={DEFAULT_PYTHON_VERSION}",
                    "-y",
                ],
                check=True,
            )
            print_colored(f"Conda environment '{env_name}' created.", Colors.OKGREEN)
        except subprocess.CalledProcessError:
            print_colored("Failed to create Conda environment.", Colors.FAIL)


def main():
    config_manager = ConfigManager(CONFIG_FILE)

    install_dependencies()
    default_repo_folder = get_or_set_default_repo_folder(config_manager)

    template_path = (
        pathlib.Path(__file__).parent.parent.resolve() / COOKIECUTTER_TEMPLATE_PATH
    )
    print_colored("Preparing to create a new project...", Colors.OKGREEN)
    repo_name = create_project_with_cookiecutter(
        template_path, default_repo_folder, config_manager
    )

    if not repo_name:
        print_colored("Project creation aborted. Exiting script.", Colors.WARNING)
        return

    project_path = pathlib.Path(default_repo_folder) / repo_name
    setup_conda_environment(project_path)
    initialize_git(project_path)

    print_colored("Project setup completed successfully.", Colors.OKGREEN)


if __name__ == "__main__":
    main()
