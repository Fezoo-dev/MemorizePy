This tiny (`literally` take a look on the screenshow below) app has been created for remembering English verbs.

![изображение](https://github.com/Fezoo-dev/MemorizePy/assets/61651027/8c7ffa5c-2373-49bc-84e7-92f6beac0c30)

It works this way: it shows a small window with one input field and one button. From time to time the app asks you a random question from its database and you need to type the answer into the input field and send your answer by clicking the button.
The app immidiately tells you ether your answer was correct or not. 
The main feature here is that the app literally talks to you! It uses internal system feature Text-To-Speech (it might require changing your PC's language settings).

For database you may use any (the most likely - csv) file that contains a list of pairs "question, answer" (separated by semicolon or comma).

I hope the app might be used not only for remembering words. For example, you can use for hosting quizes: put your questions and answers into database and the app will ask you provided questions.

I should notice that running the app requires some installed software on your PC like Python and so on, but not so much.
I've added the `install.cmd` file that should help you to cope with the installation proccess.

To start using the App run `python memorize.py` or `Memorize.vbs`
