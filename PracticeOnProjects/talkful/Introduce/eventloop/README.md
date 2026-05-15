# How to interact with the app?
## TL;DR
use stdin to send events to app:
- shortcut event
```shell
# format
shortcut {key: F1~F8} {event: PRESSED|RELEASED } \n
# example
shortcut F1 PRESSED \n
shortcut F8 RELEASED \n
```
- audio event
```shell
# format: 
voice {sample:float}
# example
voice 88.936
```
use stdout to receive the response of app:
- text inject:
```shell
# format
inject {text: str}
# example
inject hello,world!
```

## behind the scene

such a high interactive app is hard to automatically test, so we choosed to control it and receive response via stdio,
actually, the eventloop() is a infinite loop reading stdin and call those callback. and in test code, we use
multiprocessing because it provides separate memory space like subprocess, and is more controllable. and redirecting stdio
to a conn is applied since it doesn't provides stdio handling like subprocess.