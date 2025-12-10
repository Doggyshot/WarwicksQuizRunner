def runQuizzes(userName, passWord, answerKey, statusText, creditsEarnedInSession):
    from DrissionPage import ChromiumPage, ChromiumOptions, Chromium # type: ignore
    import time
    import random
    def importCaptchaSolver():
        try:
            import CaptchaSolver
        except:
            print("lite version, captcha solver not included")
    importCaptchaSolver()

    try:
        options = ChromiumOptions()     
        options.set_argument("--profile-directory=Default")
        options.incognito(True)
        
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
            return
            

        driver = ChromiumPage(addr_or_opts=options)
        driver.get("https://www.wizard101.com/game")

        statusText.set("Logging into Wizard101 website")
        time.sleep(0.5)

        driver.ele("#loginUserName").input(userName)
        driver.ele("#loginPassword").input(passWord)

        time.sleep(0.25)
        driver.ele(".override width100").click()

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
                if driver.ele(".quizQuestion", timeout=1):
                    getCorrectAnswerBox(driver, quiznames[count])
                    time.sleep(0.5)
                else:
                    break
            if driver.ele(".quizThrottle", timeout=1): # quiz already done / all quizzes done already
                statusText.set("Quiz already completed, skipping.")
                count += 1
                time.sleep(1)
                continue
            print("done")
            statusText.set("Quiz finished, confirming results.")
            driver.wait.ele_displayed(".kiaccountsbuttongreen", timeout=10)
            driver.ele(".kiaccountsbuttongreen").click(timeout=10)
            time.sleep(2)
            driver.run_js("document.querySelector('#jPopFrame_content').contentDocument.querySelector('#submit').click();")
            time.sleep(0.5)
            if CaptchaSolver:
                statusText.set("Solving Captcha")
                CaptchaSolver.SolveWizCaptcha(driver)
            creditsEarnedInSession.set(creditsEarnedInSession.get()+10)
            statusText.set("Results confirmed!")
            print("Quiz " + str(count) + " done.")
            count += 1
        
        statusText.set("Quizzes completed!")
        driver.close()

        count = 5
        while (count >= 0):
            time.sleep(1)
            statusText.set("Quizzes completed! (Closing menu in "+str(count)+")")
            count -= 1
    except Exception as e:
        if {type(e).__name__} == {'PageDisconnectedError'}:
            statusText.set("Quiz page closed, please restart quiz runner.")
            time.sleep(10)
            statusText.set("Quizzes completed! (Closing menu in 0)") # Will close the maingui, just being lazy and reusing close method.
        else:
            while True:
                statusText.set("Exception: "+str({type(e).__name__}))
                print(e)
                time.sleep(3)
                statusText.set("If you see this, please contact @doggyshot!") # please do, I will try my best respond and fix. :)
                time.sleep(3)