# -*- coding: utf-8 -*-
from code import InteractiveConsole


class EspressoConsole(InteractiveConsole, object):
    """The REPL class, for an in-terminal debug REPL"""
    def interact(self, banner=None):
        banner = """███████╗███████╗██████╗ ██████╗ ███████╗███████╗███████╗ ██████╗ 
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔═══██╗
█████╗  ███████╗██████╔╝██████╔╝█████╗  ███████╗███████╗██║   ██║
██╔══╝  ╚════██║██╔═══╝ ██╔══██╗██╔══╝  ╚════██║╚════██║██║   ██║
███████╗███████║██║     ██║  ██║███████╗███████║███████║╚██████╔╝
╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝ 
""" or banner
        super(EspressoConsole, self).interact(banner)

    def raw_input(self, prompt=''):
        prompt = '[=>]'
        return super(EspressoConsole, self).raw_input(prompt)
