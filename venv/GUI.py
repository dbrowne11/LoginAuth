import Authenticator
import Game
from tkinter import *
from functools import partial


def validate(username, password):
    """
    :param username: username field data
    :param password: password field data
    :return: True if username and password match DB, False otherwise
    """
    user = username.get()
    pswd = password.get()
    success = Authenticator.verify(user, pswd)
    if success:
        Game.play()
        return True
    else:
        print("Login Failed")
        popupLogin(False)
        return False

def popupLogin(success):
    """
    Creates a popup window to inform user of the results of their login attempt
    :param success: Boolean result of login
    :return: None
    """
    win = Toplevel()
    win.geometry('200x75')
    if success:
        win.title("Login Successful")
        Label(win, text = "You have successfully logged in").grid(row = 0, column = 0)
    else:
        win.title("Login Failed")
        Label(win, text = "Incorrect username or password").grid(row = 0, column = 0)



def signUp():
    """
    Sign up Logic
    :return: None
    """
    def valCreds(win, user, pswd, pswdVal):
        """
        Will Create a users account if all data can be verified and meets criteria,
        Prompts a user about their incorrect data otherwise
        :param win: window for function to work on
        :param user: username field data
        :param pswd: password field data
        :param pswdVal: password Verify field data
        :return: None
        """
        valUser = Authenticator.valUsername(user.get())
        if pswd.get() == pswdVal.get():
            valPswd = Authenticator.valPassword(pswd.get())
        else:
            valPswd = False
        if valPswd and valUser:
            Authenticator.add_user(user.get(), pswd.get())
            succWin = Toplevel()
            labelSucc = Label(succWin, text = 'Account has been created').grid(row = 0, column = 0)
            win.destroy()
        elif valPswd and not valUser:
            failWin = Toplevel()
            labelFail = Label(failWin, text = 'Username taken').grid(row = 0, column = 0)
        elif valUser and not valPswd:
            failWin = Toplevel()
            labelFail = Label(failWin, text = 'Invalid Password').grid(row = 0, column = 0)
        else:
            failWin = Toplevel()
            labelFail = Label(failWin, text = 'Invalid Password and Username').grid(row = 0, column = 0)
    win = Toplevel()
    win.geometry('400x300')
    labelUsername = Label(win, text = 'Choose a Username')
    labelUsername.grid(row = 0, column = 0)
    user = StringVar()
    entryUsername = Entry(win, textvariable = user)
    entryUsername.grid(row = 0, column = 1)

    labelPassword = Label(win, text = 'Choose a Password')
    labelPassword.grid(row = 1, column = 0)
    pswd = StringVar()
    confirmPswd = StringVar(0)
    entryPassword = Entry(win, textvariable = pswd)
    entryPassword.grid(row = 1, column = 1)
    passReqs0 = Label(win, text = 'Password must contatin:').grid(row = 0, column = 2)
    passReqs1 = Label(win, text = '8 or more characters').grid(row = 1, column = 2)
    passReqs3 = Label(win, text = 'at least 1 upper and lower').grid(row = 2, column = 2)
    confirmPassword = Label(win, text = 'ReEnter your password').grid(row = 2, column = 0)
    confirmEntry = Entry(win, textvariable = confirmPswd)
    confirmEntry.grid(row = 2, column = 1)

    valCreds = partial(valCreds, win, user, pswd, confirmPswd)

    finishButton = Button(win, text = "Finish SignUp", command = valCreds)
    finishButton.grid(row = 3, column = 1)


tkWindow = Tk()
tkWindow.geometry('400x300')
tkWindow.title('Login Form')

usernameLabel = Label(tkWindow, text = 'Username:')
usernameLabel.grid(row = 0, column = 0)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable = username)
usernameEntry.grid(row = 0, column = 1)

passwordLabel = Label(tkWindow, text = 'Password:')
passwordLabel.grid(row = 1, column = 0)
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable = password, show = '*')
passwordEntry.grid(row = 1, column = 1)

validate = partial(validate, username, password)

loginButton = Button(tkWindow, text = 'Login', command = validate)
loginButton.grid(row = 3, column = 0)

signUpButton = Button(tkWindow, text = 'Sign Up', command = signUp)
signUpButton.grid(row = 3, column = 1)

tkWindow.mainloop()
