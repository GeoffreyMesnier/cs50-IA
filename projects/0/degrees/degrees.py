import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    #directory = sys.argv[1] if len(sys.argv) == 2 else "small"
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # Variable pour le nombre d'exploration
    nombre_exploration = 0

    # Liste contenant la solution a retourner
    solution=[]
    # liste contenant la Solution temporaire
    temp_solution =[]
    # Creation de la node de la source
    node_debut = Node(source,parent=None,action=None)

    # Initialise la frontiere
    frontiere = StackFrontier()

    # Ajout de la node de départ a la frontiere
    frontiere.add(node_debut)

    # Creation du set d'exploration
    exploration = set()

    #  Boucle de recherche de la solution
    while True:

        # Vide la solution temporaire
        temp_solution.clear()
      
        # Test si la frontiere est vide
        if frontiere.empty():
            if len(solution) == 0:
                return None
            elif len(solution)>0:
                return solution

        # Choix d'une node dans la frontier
        node = frontiere.remove()
        print("Node en cours:", node.state)

        # Increment la variable d'exploration
        nombre_exploration += 1
        print(nombre_exploration)
        
        # Test si on a trouve la destination
        # On rempli les tableaux de resultat
        if node.state == target:
            node_temp = node
            actions = []
            cells = []
            while node_temp.parent is not None:
                actions.append(node_temp.action)
                cells.append(node_temp.state)
                node_temp = node_temp.parent 
            actions.reverse()
            cells.reverse()
            for element in range(len(actions)):
                temp_solution.append((actions[element], cells[element]))
            
            #Enregistrement de la solution
            # Solution vide
            if len(solution) == 0:
                solution = list(temp_solution)
            # Solution plus efficiente que la solution en cours
            elif len(temp_solution) < len(solution):
                print("Solution temporaire: ",len(temp_solution))
                print("Solution :", len(solution))
                solution =list(temp_solution)
            
        #Ajout de la node au explorer
        exploration.add(node.state)

        #Ajout des voisins a la frontiere
        for movie, person in neighbors_for_person(node.state):
            if not frontiere.contains_state(person) and person not in exploration:
                child = Node(state=person, parent=node, action=movie)
                frontiere.add(child)

    # TODO
    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()

