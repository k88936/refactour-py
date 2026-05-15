**Talkful** is a voice typer app. Its name came from the opposite of [typeless](https://www.typeless.com/), which is a
matured and polished product focused on voice input on desktop,
helpful to save time commanding (or blaming :p) code agents.

## Quick start

To startup with a project, it is a good way to read its testcases:

- [complete listen and type demo](file:///PracticeOnProjects/talkful/Introduce/tests/basic_usage.py)

(optional) tests for mocked dependencies

- [audio usage](file:///PracticeOnProjects/talkful/Introduce/tests/test_audio.py)
- [shortcut usage](file:///PracticeOnProjects/talkful/Introduce/tests/test_shortcut.py)

click **check** to run all test cases.

some red error msg is expected, since some tests are targeting invalid input and fast crash

<img src="../../../res/header.png" alt="banner">

## Mock

To make it a simple and friendly tour of refactor, it mocked most external dependencies:

- shortcut
- voice recording
- ASR(Automatic Sound Recognition)
- text inject (inject text into a focused text area)

## Other Docs

- go to `{package}/api.py` to see the more detailed doc str.
- [how to interact with the app?](file:///PracticeOnProjects/talkful/Introduce/eventloop/README.md)

