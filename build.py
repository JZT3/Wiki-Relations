import argparse
import subprocess
import sys
import logging
import json


#Creating custom exceptions
class DockerBuildFailedException(Exception):
    pass

class DockerVolumeCreationFailedException(Exception):
    pass

def read_version(version_file: str) -> str:
    try:
        with open(version_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        logging.error(f"Version file '{version_file}' not found.")
        raise

def write_version(version_file: str, version: str) -> None:
    try:
        with open(version_file, 'w') as f:
            f.write(version)
    except IOError:
        logging.error(f"Failed to write version to file '{version_file}'.")
        raise

def increment_version(part: str, version: str) -> str:
    """Increment a version number based on the given part (major, minor, patch)."""
    
    major, minor, patch = map(int, version.split('.'))
    
    increments = {
        "major": (1, 0, 0),
        "minor": (0, 1, 0),
        "patch": (0, 0, 1)
    }
    
    if part not in increments:
        raise ValueError(f"Unknown version part: {part}")
    
    increment = increments[part]

    if part == "major":
        minor = 0
        patch = 0
    elif part == "minor":
        patch = 0
    
    major += increment[0]
    minor += increment[1]
    patch += increment[2]
    
    return f"{major}.{minor}.{patch}"


def build_docker_image(version, image_name):
    cmd = ["docker", "build", "-t", f"{image_name}:{version}", "."]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        logging.error("Docker build failed!")
        raise DockerBuildFailedException("Failed to build Docker image!")

def create_docker_volume(volume_name: str) -> None:
    try:
        subprocess.run(['docker', 'volume', 'create', volume_name], check=True)
    except subprocess.CalledProcessError:
        logging.exception(f"Failed to create Docker volume '{volume_name}'.")
        raise DockerVolumeCreationFailedException
    
def run_docker_container(image_name: str, volume_path: str) -> None:
    
    cmd = ['docker', 'run']

    if volume_path:
        cmd.extend(['-v', f"{image_name}:{volume_path}"])
    
    cmd.append(image_name)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        logging.exception(f"Failed to run Docker container with image '{image_name}'.")
        raise

def remove_docker_volume(volume_name: str) -> None:
    try:
        subprocess.run(['docker', 'volume', 'rm', volume_name], check=True)
    except subprocess.CalledProcessError:
        logging.exception(f"Failed to remove Docker volume '{volume_name}'.")
        raise
    
def load_config(config_file="config.json"):
    with open(config_file, 'r') as file:
        return json.load(file)


def main():
    parser = argparse.ArgumentParser(description="Increment version and build Docker image.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--major", action="store_true", help="Increment the major version")
    group.add_argument("-i", "--minor", action="store_true", help="Increment the minor version")
    group.add_argument("-p", "--patch", action="store_true", help="Increment the patch version")

    args = parser.parse_args()
    current_version = read_version('version.txt')

    if args.major:
        new_version = increment_version("major", current_version)
    elif args.minor:
        new_version = increment_version("minor", current_version)
    else:
        new_version = increment_version("patch", current_version)

    write_version('version.txt',new_version)

    try:
        config = load_config()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load configuration: {e}")
        sys.exit(1)

    image_name = config.get("image_name")
    # Building the Docker image
    try:
        build_docker_image(new_version, image_name)
        logging.info(f"Built Docker image with tag: {image_name}:{new_version}")
    except DockerBuildFailedException as e:
        logging.error(e)
        sys.exit(1)

    volume_path = config.get("volume_path")
    if volume_path:
        try:
            run_docker_container(image_name, volume_path)
        except Exception as e:
            logging.error(f"Failed to run Docker container with volume: {e}")
            sys.exit(1)

    logging.info(f"Built Docker image with tag: {new_version}")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

    main()


