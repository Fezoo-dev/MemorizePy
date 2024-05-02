# About
This tiny (`literally` take a look on the screenshot below) app was created for remembering English verbs.

![изображение](https://github.com/Fezoo-dev/MemorizePy/assets/61651027/8c7ffa5c-2373-49bc-84e7-92f6beac0c30)

It works this way: it shows a small window with one input field and one button. From time to time the app asks you a random question from its database, you need to type the answer of the question into the input field and send it by clicking the button.
The app immediately tells you whether your answer was correct or not. 
The main feature here is that the app literally talks to you! It uses internal system feature Text-To-Speech (it might require changing your PC's language settings).

For database you may use any (the most likely - csv) file that contains a list of pairs "question, answer" (separated by semicolon or comma).

I hope the app might be used not only for remembering words. For example, you can use it for hosting quizes: put your questions and answers into a database and the app will ask you provided questions.

I should notice that running the app requires some installed software on your PC like Python and so on, but not so much.
I've added the `install.cmd` file that should help you to cope with the installation proccess.

# How to use.
1. Run `python memorize.py` (Everywhere) or `Memorize.vbs` (only on windows)).
2. After launching the app push `Add database` button and choose your `*.csv` file with questions and answers.
3. Choose a database from the dropdown list and push the `Start` button.
