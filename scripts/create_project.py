import os
import subprocess


def create_project_with_cookiecutter(template_path, project_name):
    subprocess.run(
        [
            "cookiecutter",
            template_path,
            "--no-input",
            "project_name={}".format(project_name),
        ],
        check=True,
    )


def setup_conda_environment(project_name, python_version):
    env_name = project_name.replace(" ", "_")
    subprocess.run(
        ["conda", "create", "--name", env_name, f"python={python_version}", "-y"],
        check=True,
    )
    print(
        f"Conda environment '{env_name}' created. To activate, use: conda activate {env_name}"
    )


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
    template_path = input("Enter the cookiecutter template path (local or git URL): ")
    project_name = input("Enter your project name: ")
    python_version = input(
        "Enter the Python version for the Conda environment (e.g., 3.8): "
    )

    create_project_with_cookiecutter(template_path, project_name)
    project_path = os.path.join(os.getcwd(), project_name)

    setup_conda_environment(project_name, python_version)
    initialize_git(project_path)
    setup_mlflow(project_path)

    print("Project setup completed successfully.")


if __name__ == "__main__":
    main()
