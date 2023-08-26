#!/usr/local/bin/python

import os
import yaml
import logging
import shutil
import sys


class Mytex:
    def __init__(self):
        self.config_path = os.path.join(os.path.expanduser("~"), ".config", "mytex", "config.yaml")
        self.templates_dir = os.path.join(os.path.expanduser("~"), ".config", "mytex", "templates")
        if not os.path.exists(self.templates_dir):
            script_path = os.path.realpath(__file__)
            if os.path.islink(script_path):
                script_path = os.path.realpath(os.readlink(script_path))
            shutil.copytree(os.path.join(os.path.dirname(script_path), "templates"), self.templates_dir)
        self.config = self._read_config(self.config_path)
        self.templates = self._get_templates()

    def _read_config(self, config_path):
        config_dir = os.path.dirname(config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        if not os.path.exists(config_path):
            with open(config_path, "w") as f:
                yaml.safe_dump({}, f, indent=4)

            config = {}
        else:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)

        return config

    def _get_templates(self):
        templates = {}
        for filename in os.listdir(self.templates_dir):
            template_name = os.path.splitext(filename)[0]
            templates[template_name] = os.path.join(self.templates_dir, filename)
        return templates

    def create(self):
        project_name = input("Project name: ")
        template_names = list(self.templates.keys())
        print("Available templates:")
        for index, template_name in enumerate(template_names):
            print("[{}] {}".format(index + 1, template_name))

        template_index = int(input("Select template (enter number): ")) - 1
        template_name = template_names[template_index]

        if template_name not in self.templates:
            raise ValueError("Invalid template name: {}".format(template_name))

        project_dir = os.path.join(os.getcwd(), project_name)
        if os.path.exists(project_dir):
            raise ValueError("Project already exists: {}".format(project_dir))

        os.makedirs(project_dir)
        self._copy_template(project_dir, template_name)
        self._update_config(project_dir, project_name, template_name)

    def template(self, project_dir):
        if not os.path.exists(project_dir):
            raise ValueError("Project does not exist: {}".format(project_dir))

        config = self._read_config(os.path.join(project_dir, ".mytex", "config.yaml"))
        template_name = config["template"]
        self._copy_template(project_dir, template_name)

    def _copy_template(self, project_dir, template_name):
        template_path = self.templates[template_name]
        for filename in os.listdir(template_path):
            source_path = os.path.join(template_path, filename)
            destination_path = os.path.join(project_dir, filename)
            self._render_template(source_path, os.path.join(project_dir, filename), self.config)
            shutil.copy(source_path, destination_path)
    
    @staticmethod
    def _render_template_with_config(template_string, config):
        """
        Find every substring of format <xxx>, and replace it with `config[xxx]`
        :param template_string: input template string containing tags like <xxx>
        :param config: a dictionary containing the tags and their values. The tags should be in the format <xxx>
        :type config: dict[str, str]
        :return: the template string with all tags replaced with their values.
        :rtype: str
        """
        for key in config:
            template_string = template_string.replace(f"<{key}>", config[key])
        return template_string
    
    def _render_template(self, template_path, destination_path, context):
        with open(template_path, "r") as f:
            template = f.read()
        with open(destination_path, "w") as f:
            f.write(Mytex._render_template_with_config(template, context))

    def _update_config(self, project_dir, project_name, template_name):
        config = self._read_config(os.path.join(project_dir, ".mytex", "config.yaml"))
        config["name"] = project_name
        config["template"] = template_name
        with open(os.path.join(project_dir, ".mytex", "config.yaml"), "w") as f:
            yaml.safe_dump(config, f, indent=4)


if __name__ == "__main__":
    m = Mytex()

    if len(sys.argv) == 1:
        # No command is given, so print help message
        print("Usage: mytex <command> [options]")
        print("Available commands:")
        print("  create   Create a new project")
        print("  template Switch the template of an existing project")
        print("  help     Print this help message")

    elif sys.argv[1] == "create":
        # Create a new project
        m.create()

    elif sys.argv[1] == "template":
        # Switch the template of an existing project
        m.template(sys.argv[2])

    else:
        # Invalid command
        print("Invalid command: {}".format(sys.argv[1]))
        print("Use `mytex help` to see a list of available commands.")
