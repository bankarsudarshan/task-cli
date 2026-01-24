"""
taskman.core sub-package contains the core 'buisness' logic of the application.

For eg,
    - how the different models are defined
    - the repository layer, which has the permissions and knowledge of interacting with the database/storage
    - the service layer, which processes input from controllers(in our case, os provides us the input, which
      it itself receives from the user via CLI), fetches/sends required data from/to repositories, maybe
      does further computation on the fetched data, and sends output back to controller(in our case, to os
      via print() method).
"""
