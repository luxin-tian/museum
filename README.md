# A Content Analysis Project on the Webiste of the Art Institute of Chicago

这个程序会从芝加哥艺术博物馆网站上爬取每一件展品的文字记载信息。

## Tutorials

### Install required packages

#### OS requirement
- Mac + Chrome v7.9
- Linux + Firefox v60+
- Windows needs extra steps to load the driver. 

#### Windows setup instructions

If you are using Windows OS, Download (1) the [Chrome browser](https://www.google.com/chrome/) and (2) the driver for Windows from [here](https://chromedriver.storage.googleapis.com/index.html?path=79.0.3945.36/), unsuppress and copy the driver to this repo's path, and replace the `chromedriver` file in this repo with the driver you downloaded from this website. 

This step allows the `selenium` package to controll Chrome automatically. 

```$ pip install pandas numpy selenium```

### Clone this repo
```$ git clone https://github.com/luxin-tian/museum.git```

### Change your workplace to the repo
```$ cd \path\to\this\repo```


### Start exploring the Art Institute of Chicago

You need a token to start the task. I will secretly tell you the token you need:)

On a Linux machine with Firefox v60+ installed: 

- `Select your OS (macOS/Linux): ` Input `macOS` or `Linux`
- `Would you like to run with headless mode (not displaying)? y/n: ` if input `n` the website pages will display on your desktop. Input `y` to run in headless mode and this will not interrupt your other works. 
- `please input your task token: ` 为了避免重复工作，请在每次运行前与我确认token！
- `Starting task (enter 'y' to confirm starting): ` Input `y` to start the task.  

```terminal
$ python3 auto_spidering_museum_text.py
Currently this script runs on macOS with Chrome v7.9 or Linux with Firefox
Select your OS (macOS/Linux): Linux
Would you like to run with headless mode (not displaying)? y/n: y
please input your task token: 1900_2500
Your digits are:
1900 2500
If this is not correct, please contact me and stop running this task.
Starting task (enter 'y' to confirm starting): y
Starting...

Chrome/Firefox will be automatically running on your computer.


Chrome/Firefox is running in a headless mode.
Sleep for 10s to avoid censorship. You have finished 20.0%.
Sleep for 10s to avoid censorship. You have finished 40.0%.
Sleep for 120s to avoid censorship. You have finished 60.0%.
Sleep for 10s to avoid censorship. You have finished 80.0%.
(1900, 1950) is sucessfull

...

>>> 
```

#### 应对反爬虫策略

目前该程序采用自动延迟来应对反爬虫策略，当遇到网站对于高频访问不予响应时，该程序将再延迟60分钟后由断点处重新启动，已获取的数据将会被保存。

### Outputs

已获取的数据将保存在该repo目录下的多个.csv文件中，文件名
- 以`0`开头，表示该区间内未被网站反爬虫策略中断。
- 以`1`开头，表示任务被反爬虫策略中断并触发了延迟启动，被中断的网页编号在文件名中进行了标记。

### Send back the result
There will be a .csv generated in the repo's folder. Please send it to me :_-_:

### Declaration

According to the [Terms](https://www.artic.edu/terms) of the website of the Art Institute of Chicago: 

> Except as otherwise provided above, you may not copy, distribute, modify, transmit, download, or otherwise use the contents of the Site for commercial purposes without the express prior written permission of AIC. 

Please DO NOT use this program and the content from the website of the Art Institute of Chicago for commercial purposes. The data I collected will be used for academic research. Any violation of the [Terms](https://www.artic.edu/terms) is subject to applicable laws in the United States. 
