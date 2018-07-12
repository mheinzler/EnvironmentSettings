# EnvironmentSettings

A plugin for **SublimeText 3** that allows to set environment variables in the .sublime-project file.  

- - -
## Description:

Variables set with **EnvironmentSettings** are available throughout Sublime. Builds, scripts, even other plugins can relay and use them.

For example I use it to...

* set *PYTHONPATH* and have python run successfully scripts that use my custom tools, from within Sublime. [Anaconda](https://packagecontrol.io/packages/Anaconda) picks up my *PYTHONPATH*  too and nicely present code completion on my custom code.
* Set *PATH* to point to some custom tools, for example [FabricEngine](http://fabricengine.com/)'s KL and then have a custom build that can call `kl $file` and run kl code from within Sublime
* Define all the possible custom environment variables that my project needs. (obviously!)

The very nice thing about **EnvironmentSettings** is that all the variables it sets are set per project. **EnvironmentSettings** can catch when a Sublime's project change and re-set the environment variables accordingly. Even more, if you have two or more Sublime's windows open at the same time, each time you get focus on one of them, **EnvironmentSettings** will run and re-set the variables. All this is completely transparent to the user.

- - -
## Setup Project Variables

The variables can be set in the "settings" part of a .sublime-project file.  
Here two entries can be created:

  * **env_file**   
    To point to an external shell file. If this file sets variables, those variables will be set also in Sublime.  
    Paths can be relative to the project file itself (ex: "../../env.sh")
  * **env**  
    is a dictionary. Each key:value pair will be set as environment variable.

Both the entries can, actually must, specify which operative system the variables are for.  
the possible values are the ones returned by the Python's function platform.system(). The value may change depending on the system you are but the common and most probable are:

* Linux
* Darwin (Mac OSX)
* Windows

At least one **must** be present.  
For example:
```json
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

- - -
## User Variables

Beside setting variables per project, it's also possible to set variables for all the projects and sections of Sublime.  
To do that, just open your user EnvironmentSettings.sublime-settings and set the variables in there.

To open the Users's EnvironmentSettings.sublime-settings go to Preferences -> Package Settings -> Environment Settings -> Settings (User)

example:   
User's EnvironmentSettings.sublime-settings contents
```json
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

- - -
## Settings

there are few settings you can change in EnvironmentSettings.sublime-settings:

* **print_output**  
  When this is set to true, some informations are printed out to console.  

* **set_sublime_variables**  
  If true some variables from within Sublime will be set too  
  this variables are:  
  "project_path", "project", "project_name", "project_base_name", "packages"

* **sublime_variables_prefix**  
  It may be useful to add a prefix to those variables so that they don't conflict with yours

* **sublime_variables_capitalized**  
  Those variables can be all capitalised if you wish.  
  ex: "project" -> "PROJECT"
    
**Note:**  
The variables in **env_file** are always set first. This means that **env** can potentially override what **env_file** did.

---

## Using the variables in a build_system

Once you have set the variables with EnvironmentSettings, you can use it in many different ways.
One common use for them is in Sublime's builds.

Imagine you have set a variable called `MY_TEST_VARIABLE` set to `Hello World!!`, then you can have:
```json
{
    "name": "Super Test",
    "shell_cmd": "echo %MY_TEST_VARIABLE%"
}
```
In any window open in Sublime, launching the `Super Test` builder, and the result will be exactly `Hello World!!`

![evtest2.png](https://bitbucket.org/repo/LgX876/images/3702956587-evtest2.png)

![evtest.png](https://bitbucket.org/repo/LgX876/images/3731143133-evtest.png)

as you can see in the images above, all can be done inside a sublime-project file, like this:


```json
{
	"build_systems":
	[
		{
			"name": "Super Test",
			"shell_cmd": "echo %MY_TEST_VARIABLE%"
		}
	],
	"folders":
	[
		{
			"path": "."
		}
	],
	"settings":
	{
		"env":
		{
			"Windows":
			{
				"MY_TEST_VARIABLE": "Hello World!!"
			}
		}
	}
}
```

### A small advise if you work on Linux or Mac

The example above was for Windows, you can do the same for Linux and Mac obviously, but you have to be sure you escape the variable.


```json
{
	"build_systems":
	[
		{
			"name": "Super Test",
			"shell_cmd": "echo \\$MY_TEST_VARIABLE"
		}
	],
	"folders":
	[
		{
			"path": "."
		}
	],
	"settings":
	{
		"env":
		{
			"Darwin":
			{
				"MY_TEST_VARIABLE": "Hello World!!"
			}
		}
	}
}
```

Note the double backslash before `$MY_TEST_VARIABLE`. This is extremely important.
An excerpt from Sublime documentation that explains why:

> **Variables**
>
> [Sublime's] variables will be expanded within any string specified in the "cmd", "shell_cmd" or "working_dir" options.
>
> If a literal $ needs to be specified in one of these options, it must be escaped with a \. Since JSON uses backslashes for escaping also, $ will need to be written as **\\\\$**

- - -
## Installation

#### Using Package Control:

Go to Preferences -> Package Control -> Install Package then type into the text-box "Environment Settings"

Click on it, the package will be installed and ready for use.

#### Using Mercurial:

Locate your Sublime Text Packages directory by using the menu item Preferences -> Browse Packages.

While inside the Packages directory, clone EnvironmentSettings in it:

hg clone https://bitbucket.org/daniele-niero/environmentsettings