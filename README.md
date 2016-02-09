EnvironmentSettings
===
A plugin for **SublimeText 3** that allows to set environment variables in the .sublime-project file.
- - -

Description:
---

Variables set with **EnvironmentSettings** are available throughout Sublime. Builds, scripts, even other plugins can relay and use them.

For example I use it to...

  * set *PYTHONPATH* and have python run successfully scripts that use my custom tools, from within Sublime. [Anaconda](https://packagecontrol.io/packages/Anaconda) picks up my *PYTHONPATH*  too and nicely present code completion on my custom code.
  
  * Set *PATH* to point to some custom tools, for example [FabricEngine](http://fabricengine.com/)'s KL and then have a custom build that can call `kl $file` and run kl code from within Sublime

  * Define all the possible custom environment variables that my project needs. (obviously!)

The very nice thing about **EnvironmentSettings** is that all the variables it sets are set per project. **EnvironmentSettings** can catch when a Sublime's project change and re-set the environment variables accordingly. Even more, if you have two or more Sublime's windows open at the same time, each time you get focus on one of them, **EnvironmentSettings** will run and re-set the variables. All this is completely transparent to the user.

Setup Project Variables
---

The variables can be set in the "settings" part of a .sublime-project file.
Here two entries can be created:

  * **env_file** to point to an external shell file. If this file sets variables, those variables will be set also in Sublime.
    Paths can be relative to the project file itself (ex: "../../env.sh")
  * **env** is a dictionary. Each key:value pair will be set as environment variable.

Both the entries can, actually must, specify which operative system the variables are for.
the possible values are the ones returned by the Python's function platform.system(). The value may change depending on the system you are but the common and most probable are:

* Linux
* Darwin (Mac OSX)
* Windows

At least one must be present.

For example:
```
#!json
{
  "folders":
  [
    {
      "path": "my/path"
    }
  ],
  "settings":
  {
    "env_file": 
    {
      "Windows": "%HOME%/Documents/myEnv.bat",
      "Darwin": "~/Documents/myEnv.sh",
      "Linux": "~/Documents/myEnv.sh"
    },
    "env":
    {
      "Windows": 
      {
        "PATH": "%PATH%;%HOME%/Documents/MyTool"
      },
      "Darwin": 
      {
        "PATH": "$PATH:~/Documents/MyTool"
      },
      "Linux": 
      {
        "PATH": "$PATH:~/Documents/MyTool"
      }
    }
  }
}
```

User Variables
---

Beside setting variables per project, it's also possible to set variables for all the projects and sections of Sublime.
To do that, just open your user EnvironmentSettings.sublime-settings and set the variables in there.

To open the Users's EnvironmentSettings.sublime-settings go to Preferences -> Package Settings -> Environment Settings -> Settings (User)

example:
```
#!json
// User's EnvironmentSettings.sublime-settings contents
{
  "print_output": true,
  "env_file": 
  {
    "Windows": "%HOME%/Documents/myEnv.bat",
    "Darwin": "~/Documents/myEnv.sh",
    "Linux": "~/Documents/myEnv.sh"
  },
  "env":
  {
    "Windows": 
    {
      "PATH": "%PATH%;%HOME%/Documents/MyTool"
    },
    "Darwin": 
    {
      "PATH": "$PATH:~/Documents/MyTool"
    },
    "Linux": 
    {
      "PATH": "$PATH:~/Documents/MyTool"
    }
  }
}
```

Settings
---

there is only one custom settings to change in EnvironmentSettings.sublime-settings and it's for debugging porpoises:

**print_output**

When this is set to true, some informations are printed out to console.

Note
---

The variables in **env_file** are always set first. This means that **env** can potentially override what **env_file** did.

Installation
---

#### Using Package Control:

Go to Preferences -> Package Control -> Install Package then type into the text-box "Environment Settings"

Click on it, the package will be installed and ready for use.

#### Using Mercurial:

Locate your Sublime Text Packages directory by using the menu item Preferences -> Browse Packages.

While inside the Packages directory, clone EnvironmentSettings in it:

hg clone https://bitbucket.org/daniele-niero/environmentsettings