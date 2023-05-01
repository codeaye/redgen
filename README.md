
# RedGen 🐙

The project involves the creation of a video that utilizes Text-to-Speech (TTS) to narrate the content of a post from the Reddit through an interactive CLI.


![Logo](assets/git/banner.jpg)

<a href="https://www.buymeacoffee.com/codaye" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>



## Demo

[This youtube channel](https://www.youtube.com/channel/UCr2OQ-RCnOiIpMNN27YXqPA) contains purely content made by this project.


## Requirements

- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [FFMPEG](https://ffmpeg.org/)
- [Firefox](https://www.mozilla.org/en-GB/firefox/new/)
- [Git](https://git-scm.com/)
- 2 Braincells

Also make sure you have a terminal that supports colours cus I spent hours making this nice to look at 😭

Brew command to install all of this:
```bash
  brew install python poetry ffmpeg git \
    && brew install --cask firefox
```
## Installation

***If at any point in any of the steps, you face errors, please read the FAQ first***

Clone the project

```bash
  git clone https://github.com/codeaye/redgen.git
```

Go to the project directory

```bash
  cd redgen
```

Install dependencies

```bash
  poetry install --without dev
```

Now to set up the project

```bash
  poetry run install.py
```
And follow along with the script

*If you wish to use the offline tts, which relies on [pyttsx3](https://github.com/nateshmbhat/pyttsx3) please make sure you meet their [requirements](https://github.com/nateshmbhat/pyttsx3) and if you are not on macos please change it's settings at `src/config.py` under the `TtsOptions` class.*

## Usage

```bash
  poetry run ./src/main.py
```
And follow along with the CLI and it will produce an output.mp4

To add more background videos, simply download them and put them in `assets/backgrounds`

*The id of a submission refers to the code in the url*

*eg: `1344yk4`*

## FAQ
### Questions
#### Why was this made?
I was bored.
#### There are already projects that can do this, what is special about this one?
Nothing really... Also I was bored.
#### Why python?
I was planning to use rust, but the only setback being the excellent library that is moviepy.
#### Does this work offline?
No it does not, it requires the internet to fetch details about the post.

### Common Errors
#### `[Errno 13] Permission denied: 'file'`
This is caused due to the linux/mac os not recognising the files as an executable. To fix run this:
```bash
  chmod +x install.py ./src/main.py
```

#### `selenium.common.exceptions.JavascriptException: Message: SyntaxError: unexpected token: identifier`
I still don't know what causes this as it is very rare, but just re-run the program and it should be fine.

*If you see any other errors, please post it in the issues page so I can help!*
## Contributing

Contributions are always welcome!

If you feel like the project is missing a feature, feel free to add it in yourself!

I may not always respond quickly as im still a student and am busy but I will respond when I can 😩.


## License

[MIT](https://choosealicense.com/licenses/mit/)

