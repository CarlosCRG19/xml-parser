import pandas as pd
from xml.dom import minidom


class XML:
    """
    Class that saves an XML file as a tree structure (where each node is an object) via the DOM API

    Attributes:
        path (str): string that indicates the location of the XML file
        dom (minidom.Document): XML file saved as tree structure. It requires the use of the parse() function
    """

    def __init__(self, path):
        self.path = path
        self.dom = minidom.parse(path)

    def get_children(self, tag):
        """
        Creates a data frame with all the child elements of a certain tag (with their attributes and text)  

        Arguments:
            tag (str): the name of the parent node from which you want to find its children
        
        Returns:
            output_df (pandas.DataFrame): dataframe where each row corresponds to the information of a child node (the first column specifies its tag)
        """

        elements = self.dom.getElementsByTagName(tag) # list of all elements with the selected tag

        if len(elements) == 0:
            print("This tag is not present in the document")
            return None

        df_columns = ['tag']
        rows = []  # list to store all the rows for the dataframe. Later on, the dataframe will be built from it

        for element in elements:

            if len(element.childNodes) == 0:
                print("No children found")
                return None

            for child in element.childNodes:

                if child.nodeType == minidom.Node.ELEMENT_NODE: # verify that each child node is an element by itself
                    row = {}
                    row['tag'] = child.tagName
                    for attribute, value in child.attributes.items(): # attributes.items() returns a list of tuples where the first element is the name of the attribute and the second is its value for this node
                        if attribute not in df_columns:
                            df_columns.append(attribute)
                        row[attribute] = value
                    row['text'] = child.firstChild.data # extract data (text) from the node
                    rows.append(row)

            df_columns.append('text')

        output_df = pd.DataFrame(rows, columns=df_columns)
        return output_df

    def xml_query(self, tag, attribute=None, value=None):
        """
        Method to perform a specific query on the document. Only the tag is a mandatory argument,
        but a single attribute can be included (elements that contain this attribute are filtered) or an attribute and a value.

        Arguments:
            tag (str): label that defines the requested class of elements
            attribute (str): optional argument indicating a characteristic to filter on elements
            value (str): specific value for the attribute. Only the elements that contain it are considered for the dataframe
        
        Returns:
            output_df (pandas.DataFrame): dataframe where each row corresponds to the information of an individual element
        """

        elements = self.dom.getElementsByTagName(tag) # list of all elements with the selected tag

        if len(elements) == 0:
            print("This tag is not present in the document")
            return None

        df_columns = []
        rows = [] # list to store all the rows for the dataframe. Later on, the dataframe will be built from it
        for element in elements:
            row = {} # dictionary to store the values for each column

            if (attribute != None) and (not element.hasAttribute(attribute) or value != None and element.getAttribute(attribute) != value): # boolean operation that verifies that the conditions of the arguments are satisfied. If not, the loop jumps to the next element

                continue

            for attb, val in element.attributes.items():
                if attb not in df_columns:
                    df_columns.append(attb)
                row[attb] = val
            row['text'] = element.firstChild.data
            rows.append(row)
        df_columns.append('text')

        output_df = pd.DataFrame(rows, columns=df_columns)
        return output_df
