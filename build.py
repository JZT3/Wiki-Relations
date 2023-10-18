import argparse
import os
import sys

def read_version(filename="version.txt"):
    with open(filename, 'r') as file:
        return file.read().strip()

def write_version(version, filename="version.txt"):
    with open(filename, 'w') as file:
        file.write(version)

def increment_version(part, version):
    major, minor, patch = map(int, version.split('.'))
    
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"Unknown version part: {part}")

    return f"{major}.{minor}.{patch}"

def build_docker_image(version):
    result = os.system(f"docker build -t your_image_name:{version} .")
    if result != 0:
        raise Exception("Docker build failed!")

def create_docker_volume(volume_name):
    result = os.system(f"docker volume create {volume_name}")
    if result != 0:
        raise Exception(f"Failed to create Docker volume: {volume_name}")

def run_docker_container(image_name, volume_name):
    result = os.system(f"docker run -v {volume_name}:/GraphTheoryProject/Wiki-Relations/src {image_name}")
    if result != 0:
        raise Exception(f"Failed to run Docker container with image: {image_name}")

def remove_docker_volume(volume_name):
    result = os.system(f"docker volume rm {volume_name}")
    if result != 0:
        raise Exception(f"Failed to remove Docker volume: {volume_name}")


def main():
    parser = argparse.ArgumentParser(description="Increment version and build Docker image.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--major", action="store_true", help="Increment the major version")
    group.add_argument("-i", "--minor", action="store_true", help="Increment the minor version")
    group.add_argument("-p", "--patch", action="store_true", help="Increment the patch version")
    group.add_argument("-v", "--volume", action="store_true", help="Increment the patch version")


    args = parser.parse_args()

    current_version = read_version()

    if args.major:
        new_version = increment_version("major", current_version)
    elif args.minor:
        new_version = increment_version("minor", current_version)
    else:
        new_version = increment_version("patch", current_version)

    write_version(new_version)
    
    try:
        build_docker_image(new_version)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Built Docker image with tag: your_image_name:{new_version}")

if __name__ == "__main__":
    main()


