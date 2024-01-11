import sqlite3
from PyQt5 import uic, QtWidgets

# function to call the first screen
def callFirstScreen():
    registrationScreen.close()
    firstScreen.label_4.setText("")
    firstScreen.lineEdit.setText("")
    firstScreen.lineEdit_2.setText("")
    firstScreen.show()

# function to call the second screen where you are logged
def callSecondScreen():
    firstScreen.label_4.setText("")
    userName = firstScreen.lineEdit.text()
    password = firstScreen.lineEdit_2.text()
    base = sqlite3.connect('registrationBase.db')
    cursor = base.cursor()

    # validate if your datas are correct or not
    try:
        cursor.execute("SELECT password FROM registration WHERE login = '{}'".format(userName))
        passwordBD = cursor.fetchone()
        if passwordBD :
            if password == passwordBD[0]:
                firstScreen.close()
                secondScreen.show()
            else:
                firstScreen.label_4.setText("Login ou senha incorretos!")
        else:
            firstScreen.label_4.setText("Usuario não encontrado.")
    except sqlite3.Error as erro:
        print("Erro na validação do login: ", erro)
        firstScreen.label_4.setText("Erro na validação do login.")
    
    base.close()


# function to loggout of the account and go to the first screen
def logout():
    secondScreen.close()
    firstScreen.label_4.setText("")
    firstScreen.lineEdit.setText("")
    firstScreen.lineEdit_2.setText("")
    firstScreen.show()


# this screen is where you will register a new account
def openRegistrationScreen():
    registrationScreen.label_2.setText("")
    registrationScreen.lineEdit.setText("")
    registrationScreen.lineEdit_2.setText("")
    registrationScreen.lineEdit_3.setText("")
    registrationScreen.lineEdit_4.setText("")
    registrationScreen.show()


# sistem of registration and validate if has a user already exists
def registration():
    name = registrationScreen.lineEdit.text()
    login = registrationScreen.lineEdit_2.text()
    password = registrationScreen.lineEdit_3.text()
    r_password = registrationScreen.lineEdit_4.text()

    if userExists(login):
        registrationScreen.label_2.setText('Usuário já cadastrado.')
        return

    # verify if the password is equal with the second password
    if (password == r_password):
        try:
            base = sqlite3.connect('registrationBase.db')
            cursor = base.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS registration (name text, login text, password text)")
            cursor.execute("INSERT INTO registration VALUES ('"+name+"','"+login+"','"+password+"')")

            base.commit()
            base.close()
            registrationScreen.label_2.setText("Usuario cadastrado com sucesso!")
        
        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ", erro)

    else:
        registrationScreen.label_2.setText("As senhas não coincidem.")


# function to verify in the database if the user already exists before to registrate a new user
def userExists(login):
    base = sqlite3.connect('registrationBase.db')
    cursor = base.cursor()
    cursor.execute("SELECT * FROM registration WHERE login = ?", (login,))
    userExists = cursor.fetchone()
    base.close()
    return userExists is not None


# calling the functions
app = QtWidgets.QApplication([])
firstScreen = uic.loadUi("primeira_tela.ui")
secondScreen = uic.loadUi("segunda_tela.ui")
registrationScreen = uic.loadUi("cadastro_tela.ui")
firstScreen.pushButton.clicked.connect(callSecondScreen)
secondScreen.pushButton.clicked.connect(logout)
firstScreen.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
firstScreen.pushButton_2.clicked.connect(openRegistrationScreen)
registrationScreen.pushButton.clicked.connect(registration)
registrationScreen.pushButton_2.clicked.connect(callFirstScreen)


firstScreen.show()
app.exec()
