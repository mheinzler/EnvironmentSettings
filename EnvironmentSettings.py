import os
import re
import copy
import platform
import sublime, sublime_plugin

sDEFAULT_ENV = copy.deepcopy(os.environ) #{}


def get_settings(settings):
    envs_file_dict = settings.get('env_file')
    envs_dict = settings.get('env')

    envs_file = None
    envs = None
    if envs_file_dict and platform.system() in envs_file_dict:    
        envs_file = os.path.expanduser(envs_file_dict[platform.system()])
    if envs_dict and platform.system() in envs_dict:
        envs = envs_dict[platform.system()]

    return (envs_file, envs)
    

def collect_variables(settings):
    envs_file, envs = get_settings(settings)

    window = sublime.active_window()
    sublime_vars = window.extract_variables()

    savedPath = os.getcwd()

    if "project_path" in sublime_vars:
        project_path = sublime_vars["project_path"]
        os.chdir(sublime_vars["project_path"])

    variables_set = ["",[],[],[]]

    # Set variables from within sublime (that are available only in builds and plugins)
    # note: we will collect only those variables that actually makes sense to have
    # avoiding for example variables sucha s "file", "file_path" or "project_extension"
    sets = sublime.load_settings("EnvironmentSettings.sublime-settings")
    if sets.get('set_sublime_variables'):
        keys = ["project_path", "project", "project_name", "project_base_name", "packages"]
        prefix = sets.get('sublime_variables_prefix', default='')
        capit = sets.get('sublime_variables_capitalized', default=False)
        for key in keys:
            env_key = prefix+key
            if capit:
                env_key = env_key.upper()  
            variables_set[1].append((env_key, sublime_vars[key]))

    # collect the variables from an external file
    if envs_file:
        variables_set[0] = os.path.abspath(envs_file)

        envf = open(os.path.abspath(envs_file), 'r')
        lines = envf.read()
        envf.close()

        if(platform.system() == "Windows"):
            cap_regex = re.compile(r"(?:(?i)set)\s([\w%$/]*)=(.+)", re.MULTILINE)
            
            it = re.finditer(cap_regex, lines)
            for m in it:
                key, value = m.groups()
                variables_set[2].append((key, value))

        else: # this is unix
            cap_regex = re.compile(r"(?:(?i)set)\s([\w%$/]*)=(?:(?![\"'])(\S*)|([\"'])(.+?)(?=\3))", re.MULTILINE)

            it = re.finditer(cap_regex, lines)
            for m in it:
                key, value, quote, quotedValue = m.groups()
                if value:
                    variables_set[2].append((key, value))
                else:
                    variables_set[2].append((key, quotedValue))
            
    # collect the variables in the dictionary "envs"
    if envs:
        for key, value in envs.items():
            variables_set[3].append((key, str(value)))

    os.chdir(savedPath)
    return variables_set


def print_result(variables_set, prefix):
    print("SYSTEM {}".format(platform.system()))
    print("SWITCH TO PROJECT: ", sublime.active_window().project_file_name())
    max_key_length = 0
    for varsets in variables_set[1:]:
        for pair in varsets:
            if len(pair[0]) > max_key_length:
                max_key_length = len(pair[0])

    log_format = '{:>'+str(max_key_length)+'} = {}'

    if len(variables_set[1]): #there are varaibles set from sublime's
        print("\n{} FROM SUBLIME:".format(prefix))
        if not variables_set[1]:
            print(('{:>'+str(max_key_length)+'}').format('None'))
        else:
            for pair in variables_set[1]:
                print( log_format.format(pair[0], pair[1]) )

    print("\n{} FROM FILE: {}".format(prefix, variables_set[0]))
    if not variables_set[0]:
        print(('{:>'+str(max_key_length)+'}').format('None'))
    else:            
        for pair in variables_set[2]:
            print( log_format.format(pair[0], pair[1]) )
    
    print("\n{}:".format(prefix))
    if not variables_set[3]:
        print(('{:>'+str(max_key_length)+'}').format('None'))
    else:   
        for pair in variables_set[3]:
            print( log_format.format(pair[0], pair[1]) )
    
    print()


# this is fired only once when the plugin gets loaded
def plugin_loaded():
    sets = sublime.load_settings("EnvironmentSettings.sublime-settings")
    
    variables_set = collect_variables(sets)

    # now set the environment with the data collected above 
    for varsets in variables_set[1:]:
        for pair in varsets:
            os.environ[pair[0]] = os.path.expandvars(pair[1])

    if sets.get('print_output'):
        print_result(variables_set, "SETTING STATIC CUSTOM ENVIRONMENT")

    global sDEFAULT_ENV
    sDEFAULT_ENV = copy.deepcopy(os.environ)


def set_project_environment():
    window = sublime.active_window()

    proj_data = window.project_data()
    if not proj_data or not 'settings' in proj_data:
        return

    # reset the environment
    sets = sublime.load_settings("EnvironmentSettings.sublime-settings")
    if sets.get('print_output'):
        print("\n\nRESET ENVIRONMENT TO DEFAULT STATE.")
    os.environ = copy.deepcopy(sDEFAULT_ENV)

    # collect the new variables
    proj_sets = proj_data['settings']
    variables_set = collect_variables(proj_sets)

    # now set the environment with the data collected above 
    for varsets in variables_set[1:]:
        for pair in varsets:
            os.environ[pair[0]] = os.path.expandvars(pair[1])

    # print out the result if the settings allow it
    if sets.get('print_output'):
        print_result(variables_set, "SETTING PROJECT ENVIRONMENT")


class ProjectEnvironmentListener(sublime_plugin.EventListener):
    def __init__(self, *args, **kwds):
        super(ProjectEnvironmentListener, self).__init__(*args, **kwds)

        self.active_project = sublime.active_window().project_file_name()

    def on_activated(self, view):
        st_version = int(sublime.version())
        if st_version < 3000:
            # before version 3 it was impossible to get access to projects settings
            return

        if self.active_project == sublime.active_window().project_file_name():
            return
        else:
            self.active_project = sublime.active_window().project_file_name()
            if self.active_project:
                set_project_environment()
                self.__change_project_data()
            else:
                sets = sublime.load_settings("EnvironmentSettings.sublime-settings")
                if sets.get('print_output'):
                    print("EnvironmentSettings: project file not found")

    def on_post_save(self, view):
        if view.file_name() == sublime.active_window().project_file_name():        
            self.__change_project_data()

    def __change_project_data(self):
        sets = sublime.load_settings("EnvironmentSettings.sublime-settings")
        data = sublime.active_window().project_data()
        for folder in data['folders']:
            # print(folder['path'])
            if "path-template" in folder:
                template = folder['path-template']
                resolved = os.path.expandvars(template)
                if sets.get('print_output'):
                    print("template {} resolved in {}".format(template, resolved)) 
                folder['path'] = resolved
        sublime.active_window().set_project_data(data)


class ForceProjectEnvironmentCommand(sublime_plugin.WindowCommand):
    def run(self):
        set_project_environment()
