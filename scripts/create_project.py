import json
import os
import pathlib
import shutil
import subprocess

config_file_path = pathlib.Path(__file__).parent.resolve() / "config.json"


def install_dependencies():
    # Check if pipx is installed
    if not shutil.which("pipx"):
        subprocess.run(["pip", "install", "pipx"], check=True)

    # Check if cookiecutter is installed via pipx
    if not shutil.which("cookiecutter"):
        subprocess.run(["pipx", "install", "cookiecutter"], check=True)


def get_or_set_default_repo_folder():
    if config_file_path.exists():
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
            return os.path.expanduser(config.get("default_repo_folder"))

    default_repo_folder = input("Enter the path for the default projects folder: ")
    default_repo_folder = os.path.expanduser(default_repo_folder)
    with open(config_file_path, "w") as config_file:
        json.dump({"default_repo_folder": default_repo_folder}, config_file)

    return default_repo_folder


def create_project_with_cookiecutter(template_path, default_repo_folder):
    project_name = input("Enter the name for the new project: ")
    repo_name = input("Enter the name for the new repository: ")
    module_name = input("Enter the name for the new module: ")
    author_name = input("Enter your name (or your organization/company/team): ")
    description = input("Enter a short description of the project: ")
    python_version = input("Enter the Python version to use (3.11): ")

    os.chdir(default_repo_folder)
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
    subprocess.run(["git", "init"], cwd=project_path, check=True)
    subprocess.run(["git", "add", "."], cwd=project_path, check=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"], cwd=project_path, check=True
    )


def main():
    install_dependencies()
    default_repo_folder = get_or_set_default_repo_folder()

    # Get the absolute path to the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Go up one level to the project root
    project_root = os.path.dirname(script_dir)

    # Append "cookiecutter-template" to it
    template_path = os.path.join(project_root, "cookiecutter-template")

    repo_name = create_project_with_cookiecutter(template_path, default_repo_folder)

    # Assume the project name is the name of the created directory
    project_path = os.path.join(default_repo_folder, repo_name)

    initialize_git(project_path)

    print("Project setup completed successfully.")


if __name__ == "__main__":
    main()
