from dataclasses import dataclass


@dataclass
class AttributeMap:
    """
    Maps column name in the .csv file to the key in the template document.
    The attribute map is accessible using the table_key.
    """

    table_key: str = ""     # Column key in the .csv file
    template_key: str = ""  # Key in the document (.docx) template


class DataEntry(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setattr__
    __delattr__ = dict.__delitem__

    def format(self):
        self.FirstName = self.FirstName.upper()
        self.LastName = self.LastName.upper()
        # self.club = self.club.upper().replace(" - ", "\n")

        match self.Division.lower():
            case "recurve":
                self.Division = "Reflexní luk"
            case "barebow":
                self.Division = "Holý luk"
            case _:
                # raise ValueError(f"Unknown division: {other}")
                pass

        self.Division = self.Division.upper()
        self.Category = self.Category.upper()

        return self
