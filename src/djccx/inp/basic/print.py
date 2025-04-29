def print(self, file="test.inp",inline=False):
    # Open the file for writing

    # Define the sections to print
    sections = [self.nodes]   + \
                self.elements + \
                self.nsets + \
                self.elsets   +\
                self.elsetsofelsets + \
                self.surfaces + \
                self.equations + \
                self.ties + \
                self.surface_interactions +\
                self.contacts + \
                self.materials + \
                self.orientations + \
                self.solid_sections + \
                self.shell_sections + \
                self.transforms + \
                self.steps 

    # Write each section to the file
    if not inline:
        file = open(file, 'w')
        for section in sections:
            section_text = section.print().replace('\r', '')
            file.write(section_text + '\n')

        # Close the file
        file.close()
    
    else:
        text = ""
        for section in sections:
            section_text = section.print().replace('\r', '')
            text += section_text + '\n'
        return text