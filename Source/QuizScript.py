def runQuizzes(userName, passWord, answerKey, statusText, creditsEarnedInSession):
    from DrissionPage import ChromiumPage, ChromiumOptions, Chromium # type: ignore
    from DrissionPage.errors import PageDisconnectedError
    import time, random, sys, os, shutil

    def clearUserDataPath():
        userDataPath = getMainPath("bin\\temp-user-data-path") # clear out user data path 
        shutil.rmtree(userDataPath)
        os.makedirs(userDataPath)

    def getMainPath(relativePath):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return os.path.dirname(sys.executable)+"\\"+relativePath
        else:
            return os.path.dirname(__file__)+"\\"+relativePath
        
    os.makedirs(getMainPath("bin\\temp-user-data-path"), exist_ok=True) # just in case it didn't get created
    

    RunningLite = True
    try:
        import CaptchaSolver
        print("CaptchaSolver imported")
        RunningLite = False
    except:
        print("lite version, captcha solver not included")

    try:
        options = ChromiumOptions()     
        options.set_argument("--profile-directory=Default")
        options.incognito(True)
        options.set_browser_path(getMainPath("bin\\chrome-win64\\chrome.exe")) # Chrome version 135
        options.set_user_data_path(getMainPath("bin\\temp-user-data-path"))  # Temp data folder for said version

        
        def getCorrectAnswerBox(page, quizName):
            questionElementText = page.ele(".quizQuestion").text
            print(questionElementText)

            quizName = quizName.replace("-", " ")
            quizName = quizName.title()
            theCorrectAnswer = ""


            for question, correctAnswer in answerKey[quizName]:
                if questionElementText == question:
                    theCorrectAnswer = correctAnswer


            page.run_js("document.querySelector('#nextQuestion').style.visibility = 'visible';")
            page.run_js("document.querySelector('.answersContainer > div:nth-child(1)').style.visibility = 'visible';")
            page.run_js("document.querySelector('.answersContainer > div:nth-child(2)').style.visibility = 'visible';")
            page.run_js("document.querySelector('.answersContainer > div:nth-child(3)').style.visibility = 'visible';")
            page.run_js("document.querySelector('.answersContainer > div:nth-child(4)').style.visibility = 'visible';")

            answerCount = 0

            answer_texts = page.eles(".answerText")
            for textElements in answer_texts:
                if textElements.text == theCorrectAnswer:
                    page.eles(".largecheckbox")[answerCount].click()
                    page.ele("#nextQuestion").click()
                    return
                else:
                    answerCount += 1
            page.eles(".largecheckbox")[1].click() # if correct answer isn't found, just pick the first option to avoid hanging
            page.ele("#nextQuestion").click()
            return
            

        driver = ChromiumPage(addr_or_opts=options)
        print(driver.browser.version)
        driver.get("https://www.wizard101.com/game")
        time.sleep(1)
        driver.get("https://www.wizard101.com/game")

        statusText.set("Logging into Wizard101 website")
        time.sleep(0.5)

        driver.ele("#loginUserName").input(userName)
        driver.ele("#loginPassword").input(passWord)

        time.sleep(0.25)
        driver.ele(".override width100").click()

        time.sleep(1)
        if not RunningLite:
            captchaResult = CaptchaSolver.SolveWizCaptcha(driver, True)
        if RunningLite or captchaResult == "CaptchaUncompleted":
            statusText.set("Captcha unsuccessful, please finish login manually.")
            loginSuccessful = False
            while not loginSuccessful: # loop check for the login button until its gone (successful login)
                loginButton = driver.ele(".override width100", timeout= 1.0)
                if loginButton:
                    continue
                loginSuccessful = True

        time.sleep(1)
        statusText.set("Starting quizzes...")

        quiznames = []
        for quiz in answerKey:
            quiz = quiz.replace(" ", "-")
            quiznames.append(quiz)
        
        random.shuffle(quiznames) #not sure if this helps avoid getting detected, but might as well
        count = 0

        print('quiz farmer started')
        while (count < 10):
            driver.get('https://www.wizard101.com/quiz/trivia/game/'+quiznames[count]+'-trivia')
            statusText.set("Completing "+quiznames[count].replace("-", " ")+" quiz ("+str(count+1)+" of 10)")
            
            while True:
                if driver.ele(".quizQuestion", timeout=1.0):
                    getCorrectAnswerBox(driver, quiznames[count])
                    time.sleep(0.5)
                else:
                    break
            if driver.ele(".quizThrottle", timeout=1.0): # quiz already done / all quizzes done already
                statusText.set("Quiz already completed, skipping.")
                count += 1
                time.sleep(1)
                continue
            print("done")
            statusText.set("Quiz finished, confirming results.")
            driver.wait.ele_displayed(".kiaccountsbuttongreen", timeout=10.0)
            driver.ele(".kiaccountsbuttongreen").click(timeout=10.0)
            time.sleep(2)
            driver.run_js("document.querySelector('#jPopFrame_content').contentDocument.querySelector('#submit').click();")
            time.sleep(0.5)
            if not RunningLite:
                statusText.set("Solving Captcha")
                captchaResult = CaptchaSolver.SolveWizCaptcha(driver, False)
            if RunningLite or captchaResult == "CaptchaUncompleted":
                statusText.set("Captcha unsuccessful, please finish captcha manually.")
                quizSuccessful = False
                while not quizSuccessful: # loop check for the "see your score" button until its gone (quiz registered)
                    blueButtons = driver.eles(".kiaccountsbuttonblue", timeout= 1.0)
                    if len(blueButtons) == 2: # check if blue score button disappears (Another unrelated invisible blue button exists on the page)
                        continue
                    quizSuccessful = True
            time.sleep(1)
            creditsEarnedInSession.set(creditsEarnedInSession.get()+10)
            statusText.set("Results confirmed!")
            print("Quiz " + str(count) + " done.")
            count += 1
        
        statusText.set("Quizzes completed!")
        driver.close()
        clearUserDataPath()

        count = 5
        while (count >= 0):
            time.sleep(1)
            statusText.set("Quizzes completed! (Closing menu in "+str(count)+")")
            count -= 1
    except PageDisconnectedError: # chrome tab was closed
        clearUserDataPath()
        statusText.set("Quiz page closed, please restart quiz runner.")
        time.sleep(10)
        statusText.set("Quizzes completed! (Closing menu in 0)") # Will close the maingui, just being lazy and reusing close method.
    
    except Exception as e:
        clearUserDataPath()
        while True:
            statusText.set("Exception: "+str({type(e).__name__}))
            print(e)
            time.sleep(3)
            statusText.set("If you see this, please contact @doggyshot!") # please do, I will try my best respond and fix. :)
            time.sleep(3)