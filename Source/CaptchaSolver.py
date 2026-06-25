def SolveWizCaptcha(driver, IsLogin = bool):
    try: 
        from DrissionPage.common import Keys
        import time
        import urllib.request
        from whisper import load_model
        import os

        BASE_DIR = os.path.dirname(__file__)

 
        iframe = driver.get_frame("@id=jPopFrame_content", timeout=2.0)
        if iframe:
            if IsLogin: # extra step for login recaptcha
                iframe2 = iframe.get_frame("@title=reCAPTCHA", timeout=2.0)
                time.sleep(1)
                iframe2.run_js('document.querySelector("#recaptcha-anchor > div.recaptcha-checkbox-border").click();')

            iframe2 = iframe.get_frame("@title=recaptcha challenge expires in two minutes", timeout=1.0)
            print(iframe2)
            if iframe2:
                iframe2 = iframe.get_frame("@title=recaptcha challenge expires in two minutes")
                time.sleep(1)
                iframe2.wait.ele_displayed("#recaptcha-audio-button", timeout=2.0)
                iframe2.ele("#recaptcha-audio-button").click()
                time.sleep(2)
                AudioLink = iframe2.ele("#audio-source").attr('src')
                time.sleep(1)
                newfile = urllib.request.urlretrieve(AudioLink)
                print(newfile[0])
                print(BASE_DIR+r"\bin\tiny.pt")

                whisperModel = load_model(BASE_DIR+r"\bin\tiny.pt")
                result = whisperModel.transcribe(newfile[0])
                print(result["text"])
                iframe2.ele("#audio-response").input(result["text"])
                time.sleep(1)
                iframe2.ele("#audio-response").input(Keys.ENTER)
        else:
            print("No Captcha detected.")
            return "NoCaptchaDetected"
    except Exception as e:
        print("Could not complete Captcha, please manually complete")
        return "CaptchaUncompleted"