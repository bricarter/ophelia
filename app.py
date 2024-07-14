from sys import argv

import requests


def organize_output(output):
    for project in output:
        print()
        print(project)
        print("-------------------------")
        for dependency in output[project]:
            print(f"{dependency} | installed: {output[project][dependency]['installed']} | latest: {output[project][dependency]['latest_release']}")


def get_release(dependency):
    """ Return the latest release of a dependency. """
    pypi_response = requests.get(f"https://pypi.org/pypi/{dependency}/json")
    latest_release = pypi_response.json()["info"]["version"]
    return latest_release
    

def get_dependencies(project):
    """ 
    Return an object containing each dependency name, installed version, and latest release. 
    
    dependencies = {
            dependency_one: 
                {
                installed: <installed_version>, 
                latest_release: <latest_release_version>
                }, 
            dependency_two:
                {
                installed: <installed_version>, 
                latest_release: <latest_release_version>
                },
            ...
            }
    """
    dependencies = {}

    with open(project, "r") as requirements:
        for dependency in requirements:
            name = dependency[:dependency.rfind("==")]

            dependencies[name] = {"installed": dependency[dependency.rfind("=")+1:], "latest_release": get_release(name)}

    return dependencies


def main():
    check_list = argv[1]
    output = {}

    with open(check_list, "r") as projects:
        for project in projects.read().splitlines():
            output[project] = get_dependencies(project)

    organize_output(output)




if __name__ == "__main__":
    main()