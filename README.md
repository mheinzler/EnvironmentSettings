# EnvironmentSettings #

### Description: ###

A plugin for **SublimeText 3** that allows to set environment variables in the .sublime-project file.

The variables can be set in the "settings" part of a .sublime-project file.
Here two entries can be created:

* **env_files** to point to an external shell file. If this file sets variables, those variables will be set also in Sublime.
* **env** is a dictionary. Each key:value pair will be set as environment variable.

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
    "env_file": "~/Documents/myEnv.sh",
    "env":
    {
      "PATH": "%PATH%:~/Documents/MyTool"
    }
  }
}
```

### Note: ###

The variables in "env_files" are always set first. This means that "env" can potentially override what "env_file" did.