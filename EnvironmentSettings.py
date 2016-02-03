import os
import re
import copy
import platform
import sublime, sublime_plugin

sDEFAULT_ENV = {}


def get_settings(settings):
    envs_file_dict = settings.get('env_file')
    envs_dict = settings.get('env')

    envs_file = None
    envs = None
    if envs_file_dict and platform.system() in envs_file_dict:
        envs_file = envs_file_dict[platform.system()]
    if envs_dict and platform.system() in envs_dict:
        envs = envs_dict[platform.system()]

    return (envs_file, envs)
    

def collect_variables(settings):
    envs_file, envs = get_settings(settings)

    savedPath = os.getcwd()
    os.chdir(os.path.dirname(sublime.active_window().project_file_name()))

    variables_set = ([],[])

    # collect the variables from an external file
    if envs_file:
        cap_regex = re.compile("^(?:(?i)export|set)\s([a-zA-Z0-9%_$/]*)\=([a-zA-Z0-9%$_\-~/\\\;:\.]+)", re.M|re.X|re.S)
        envf = open(os.path.abspath(envs_file), 'r')
        lines = envf.read()
        envf.close()

        it = re.finditer(cap_regex, lines)
        
        for m in it:
            key, value = m.groups()
            variables_set[0].append((key, value))

    # collect the variables in the dictionary "envs"
    if envs:
        for key, value in envs.items():
            variables_set[1].append((key, value))

    os.chdir(savedPath)
    return variables_set


def print_result(variables_set, prefix):
    print("SYSTEM {}".format(platform.system()))
    print("SWITCH TO PROJECT: ", sublime.active_window().project_file_name())
    max_key_length = 0
    for varsets in variables_set:
        for pair in varsets:
            if len(pair[0]) > max_key_length:
                max_key_length = len(pair[0])

    log_format = '{:>'+str(max_key_length)+'} = {}'

    print("\n{} FROM FILE:".format(prefix))
    for pair in variables_set[0]:
        print( log_format.format(pair[0], pair[1]) )
    
    print("\n{}:".format(prefix))
    for pair in variables_set[1]:
        print( log_format.format(pair[0], pair[1]) )
    
    print()


# this is fired only once when the plugin gets loaded
def plugin_loaded():
    os.environ["SUBLIME_ACTIVE_PROJECT"] = "" #sublime.active_window().project_file_name()

    sets = sublime.load_settings("EnvironmentSettings.sublime-settings")
    
    variables_set = collect_variables(sets)

    # now set the environment with the data collected above 
    for varsets in variables_set:
        for pair in varsets:
            os.environ[pair[0]] = os.path.expandvars(pair[1])

    if sets.get('print_output'):
        print_result(variables_set, "SETTING STATIC CUSTOM ENVIRONMENT")

    global sDEFAULT_ENV
    sDEFAULT_ENV = copy.deepcopy(os.environ)



class ProjectEnvironmentListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        st_version = int(sublime.version())
        if st_version < 3000:
            # before version 3 it was impossible to get access to projects settings
            return

        if "SUBLIME_ACTIVE_PROJECT" in os.environ and \
           os.environ["SUBLIME_ACTIVE_PROJECT"] == sublime.active_window().project_file_name():
            return
        else:
            # reset the environment
            sets = sublime.load_settings("EnvironmentSettings.sublime-settings")
            if sets.get('print_output'):
                print("\nRESET ENVIRONMENT TO DEFAULT STATE.")
            os.environ = copy.deepcopy(sDEFAULT_ENV)
            project_name = sublime.active_window().project_file_name()
            if project_name:
                os.environ["SUBLIME_ACTIVE_PROJECT"] = sublime.active_window().project_file_name()
                self.set_project_environment()
            else:
                os.environ["SUBLIME_ACTIVE_PROJECT"] = ""
                if sets.get('print_output'):
                    print("EnvironmentSettings: project file not found")


    def set_project_environment(self):
        window = sublime.active_window()
        proj_data = window.project_data()
        if not proj_data or not 'settings' in proj_data:
            return

        proj_sets = proj_data['settings']
        variables_set = collect_variables(proj_sets)

        # now set the environment with the data collected above 
        for varsets in variables_set:
            for pair in varsets:
                os.environ[pair[0]] = os.path.expandvars(pair[1])

        # print out the result if the settings allow it
        sets = sublime.load_settings("EnvironmentSettings.sublime-settings")
        if sets.get('print_output'):
            print_result(variables_set, "SETTING PROJECT ENVIRONMENT")
        


class EnvSetCheckCommand(sublime_plugin.WindowCommand):
    def run(self, edit):
        print(sDEFAULT_ENV)
        print(sDEFAULT_ENV==os.environ)
        