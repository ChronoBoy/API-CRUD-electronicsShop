
class CustomExceptionUser(Exception):
    def __init__(self,userName,userEmail):
        self.userName = userName
        self.userEmail = userEmail
    
    def imprimir(self):
        return self.userName



