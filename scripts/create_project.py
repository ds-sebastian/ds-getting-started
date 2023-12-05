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
            return config.get("default_repo_folder")

    default_repo_folder = input("Enter the path for the default projects folder: ")
    with open(config_file_path, "w") as config_file:
        json.dump({"default_repo_folder": default_repo_folder}, config_file)

    return default_repo_folder


def create_project_with_cookiecutter(template_path, default_repo_folder):
    os.chdir(default_repo_folder)
    subprocess.run(["cookiecutter", template_path], check=True)


def initialize_git(project_path):
    subprocess.run(["git", "init"], cwd=project_path, check=True)
    subprocess.run(["git", "add", "."], cwd=project_path, check=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"], cwd=project_path, check=True
    )


def setup_mlflow(project_path):
    mlflow_tracking_file = os.path.join(project_path, "MLproject")
    with open(mlflow_tracking_file, "w") as file:
        file.write("name: {}\n".format(os.path.basename(project_path)))
    print("MLflow tracking file created at: " + mlflow_tracking_file)


def main():
    install_dependencies()
    default_repo_folder = get_or_set_default_repo_folder()
    template_path = input("Enter the cookiecutter template path (local or git URL): ")

    create_project_with_cookiecutter(template_path, default_repo_folder)

    # Assume the project name is the name of the created directory
    project_name = input("Enter the name of the created project: ")
    project_path = os.path.join(default_repo_folder, project_name)

    initialize_git(project_path)
    setup_mlflow(project_path)

    print("Project setup completed successfully.")


if __name__ == "__main__":
    main()
