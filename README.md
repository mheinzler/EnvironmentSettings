# EnvironmentSettings #

### Description: ###

A plugin for **SublimeText 3** that allows to set environment variables in the .sublime-project file.

The variables can be set in the "settings" part of a .sublime-project file.
Here two entries can be created:

* **env_file** to point to an external shell file. If this file sets variables, those variables will be set also in Sublime.
  Paths can be relative to the project file itself (ex: "../../env.sh")
* **env** is a dictionary. Each key:value pair will be set as environment variable.

Both the entries can, actually must, specify which operative system the variables are for.
the possible values are the same used by Sublime in configuration files:

* Linux
* OSX
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
      "OSX": "~/Documents/myEnv.sh",
      "Linux": "~/Documents/myEnv.sh"
    },
    "env":
    {
      "Windows": 
      {
        "PATH": "%PATH%;%HOME%/Documents/MyTool"
      },
      "OSX": 
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

### User Variables ###

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
    "OSX": "~/Documents/myEnv.sh",
    "Linux": "~/Documents/myEnv.sh"
  },
  "env":
  {
    "Windows": 
    {
      "PATH": "%PATH%;%HOME%/Documents/MyTool"
    },
    "OSX": 
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

### Settings: ###

there is only one custom settings to change in EnvironmentSettings.sublime-settings and it's for debugging porpoises:

**print_output**

When this is set to true, some informations are printed out to console.

### Note: ###

The variables in **env_file** are always set first. This means that **env** can potentially override what **env_file** did.

### Installation: ###

#### Using Package Control: ####

Go to Preferences -> Package Control -> Install Package then type into the text-box "Environment Settings"

Click on it, the package will be installed and ready for use.

#### Using Mercurial: ####

Locate your Sublime Text Packages directory by using the menu item Preferences -> Browse Packages.

While inside the Packages directory, clone EnvironmentSettings in it:

hg clone https://bitbucket.org/daniele-niero/environmentsettings
