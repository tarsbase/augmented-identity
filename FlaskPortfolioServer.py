from __future__ import print_function
from flask import Flask, request, redirect, url_for, render_template, Response, jsonify
import sys

app = Flask(__name__)

##user data
userDict = {'jkoch': ['james']}
currentUser = None
personalWebsite = "None"
github = []
linkedIn = "None"
facebook = "None"
skills = "None"
major = "None"

##Web pages
#initial render
@app.route('/')
def index():
    return render_template ("registerPageOffish.html")
    
# when POST method is called from register page
@app.route("/", methods = ["POST", "GET"])
def register():
    global userDict
    global currentUser
    fullName = request.form ['fullName']
    userName = request.form ['user']
    password = request.form ['pass']
    confirm = request.form ['confirmPass']
    if request.form ['button'] == "Register" and fullName != "" and \
                    userName != "" and password != "" and password == confirm:
        userDict[userName] = [None, None, [None, None, None], None, None, None, None, None]
        userDict[userName][0] = fullName
        userDict[userName][1] = password
        currentUser = userName
        
        print(userDict, file=sys.stderr)
        return redirect("/finishedRegistration")
    elif request.form ['button'] == "Or Login":
        return redirect("/loginPage")
    else:
        return redirect ("/")
        
@app.route("/loginPage")
def loginTemplate():
    return render_template("PrettyLoginPage.html")

#login screen, must check if user is in system
@app.route("/loginPage", methods = ["POST", "GET"])
def login():
    global userDict
    global currentUser
    userName = request.form ['username']
    password = request.form ['password']
    if userName not in userDict:
        return redirect("/")
    elif userName in userDict and userDict[userName][1] != password:
        return redirect("/loginPage")
    else:
        currentUser = userName
        return redirect("/viewPortfolio")
        
#redirects the registration page to the finished registration page
@app.route("/finishedRegistration")
def finishedRegistration():
    return render_template("finishedRegistration.html")

#redirects the finished registration page to the enter portfolio screen
@app.route("/finishedRegistration", methods = ["POST", "GET"])
def Continue():
    return redirect("/enterPortfolioScreen")
    
#loads the enter portfolio template
@app.route("/enterPortfolioScreen")
def enterDataScreen():
    return render_template("PrettyPortfolioInformation.html")

#retrieves the linkes and stores it with users
@app.route("/enterPortfolioScreen", methods = ["POST", "GET"])
def enterPortfolioData():
    personalWebsite = None
    github = None
    linkedIn = None
    facebook = None
    skills = None
    major = None
    global currentUser
    global userDict
    print (currentUser, file = sys.stderr)
    if request.method == "POST":
        personalWebsiteLink = request.form ["PersonalWebsite"]
        githubLink = request.form ["Github"]
        linkedInLink = request.form ["LinkedIn"]
        facebookLink = request.form ["Facebook"]
        skillsList = request.form ["Skills"]
        tmpMajor = request.form ["Major"]
        if personalWebsiteLink != "enter URL" and personalWebsiteLink != "":
            personalWebsite = personalWebsiteLink
        if githubLink != "enter URL" and githubLink != "":
            github = githubLink
        if linkedInLink != "enter URL" and linkedInLink != "":
            linkedIn = linkedInLink
        if facebookLink != "enter URL" and facebookLink != "":
            facebook = facebookLink
        if skillsList != "enter your skills" and skillsList != "":
            skills = skillsList
        if tmpMajor != "enter your major" and tmpMajor != "":
            major = tmpMajor
        print (userDict [currentUser], file = sys.stderr)
        userDict[currentUser][2][2] = github
        userDict[currentUser][3] = facebook
        userDict[currentUser][4] = linkedIn
        userDict[currentUser][5] = personalWebsite
        userDict[currentUser][6] = skills
        userDict[currentUser][7] = major
        print(request.form, file=sys.stderr)
        return render_template("PrettyPortfolioSummary.html", result = tupleList(currentUser, userDict))
        
def tupleList(user, dict):
    result = []
    if userDict[user][2] != None:
        result.append(("Github", dict[user][2][2]))
    else:
        result.append(("Github", "None"))
    result.append(("Facebook", dict[user][3]))
    result.append(("LinkedIn", dict[user][4]))
    result.append(("Personal", dict[user][5]))
    result.append(("Skills", dict[user][6]))
    result.append(("Major", dict[user][7]))
    return result
        
        
@app.route("/viewPortfolio")
def showPortfolio():
    return render_template("PrettyPortfolioSummary.html", result = tupleList(currentUser, userDict))

@app.route("/viewPortfolio", methods=["POST", "GET"])
def editPortfolioButton():
    return redirect("PrettyPortfolioSummary.html")



if __name__ == '__main__':
    app.run(debug=True, host='128.237.168.24')

