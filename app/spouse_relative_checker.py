from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
import gedcom.tags

def run_checker(file_path):
  results = "Individual Name,Spouse Name,Shared Ancestor, # of Generations Removed from Individual, # of Generations Removed from Spouse<br />"

  # Initialize the parser
  gedcom_parser = Parser()

  # Parse your file
  gedcom_parser.parse_file(file_path, False)

  root_child_elements = gedcom_parser.get_root_child_elements()

  def print_name(person):
    name = person.get_name()
    return name[0] + " " + name[1]

  def get_ancestors(person, level = 0):
    parents = gedcom_parser.get_parents(person, "ALL")
    
    for index, parent in enumerate(parents):
      parents[index] = (parent, level)
    
    ancestors = []
    ancestors.extend(parents)

    for parent in parents:
      ancestors.extend(get_ancestors(parent[0], level + 1))
    
    return ancestors

  def are_related(person_one, person_two):
    ancestors_one = get_ancestors(person_one)
    ancestors_two = get_ancestors(person_two)

    # traverse in the 1st list 
    for x in ancestors_one: 
        # traverse in the 2nd list 
        for y in ancestors_two: 
            # if one common 
            if x[0] == y[0]: 
                return (x[0], x[1], y[1])
    return False

  count = 0

  # Iterate through all root child elements
  for individual in root_child_elements:
      # Is the `element` an actual `IndividualElement`? (Allows usage of extra functions such as `surname_match` and `get_name`.)
      if isinstance(individual, IndividualElement):
        families = gedcom_parser.get_families(individual, gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE)
        for family in families:
          family_members = gedcom_parser.get_family_members(family, members_type=gedcom.tags.GEDCOM_TAG_WIFE)

          if len(family_members) > 0:
            for spouse in family_members:
              shared_ancestor_tuple = are_related(individual, spouse)
              if individual != spouse and shared_ancestor_tuple:
                results += print_name(individual) + "," + print_name(spouse) + "," + print_name(shared_ancestor_tuple[0]) + "," + str(shared_ancestor_tuple[1]) + "," + str(shared_ancestor_tuple[2]) + "<br />"
                count += 1

  results += 'Total count: ' + str(count)

  return results