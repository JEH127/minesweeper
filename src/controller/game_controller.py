class GameController:

    def __init__(self, model, view):
        self.model = model
        self.view = view  
        
        # Connect buttons in the view to their respective handler methods
        
        
        
        # Exemple de l'appli precedente pour la connection de boutons
                        
            # self.view.add_button.clicked.connect(self.add_contact)
            # self.view.modify_button.clicked.connect(self.modify_contact)
            # self.view.delete_button.clicked.connect(self.delete_contact)
            # self.view.search_bar.textChanged.connect(self.search_contacts)
            # Methods

         # Exemple de l'appli precedente pour la une fonction du controlleur quir épond à un evenement
         
            #  def add_contact(self):
            # """
            # Handles the addition of a new contact.
            # Opens a form for the user to input contact details.
            # If valid data is provided, creates a new Contact object, adds it to the model, and refreshes the contact list.
            # """
            # data = self.view.show_contact_form()
            # if data:
            #     contact = Contact(**data)
            #     self.model.add_contact(contact)
            #     self.load_contacts()
            
    '''
    JAMAL 
    After each action (click on a cell), check for defeat or victory by calling the appropriate methods from the model.
    '''
    
    '''
    Reacting to a left click on a cell: notify the model to reveal the cell and update the view accordingly
    '''
    
    
    '''
    Reacting to a right click on a cell: place (or remove) a flag, update the remaining mines count, and update the view accordingly.
    '''
    
    '''
    Initialize a new game according to the chosen difficulty (call the model's methods to generate a new grid).
    '''
    