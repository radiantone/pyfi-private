import json
import textwrap
from os import getenv
from os.path import exists
from sys import argv

# from revChatGPT.revChatGPT import Chatbot
from svglib.svglib import svg2rlg


class CaptchaSolver:
    """
    Captcha solver
    """

    @staticmethod
    def solve_captcha(raw_svg):
        """
        Solves the captcha

        :param raw_svg: The raw SVG
        :type raw_svg: :obj:`str`

        :return: The solution
        :rtype: :obj:`str`
        """
        # Get the SVG
        svg = raw_svg
        # Save the SVG
        with open("captcha.png", "w", encoding="utf-8") as f:
            print("Captcha saved to captcha.png")
            png = svg2rlg(svg)
            f.write(png)
        # Get input
        solution = input("Please solve the captcha: ")
        # Return the solution
        return solution


def consult(prompt):
    try:
        # prompt = bytes(prompt)
        prompt = str(prompt)
        config_files = ["config.json"]
        xdg_config_home = getenv("XDG_CONFIG_HOME")
        if xdg_config_home:
            config_files.append(f"{xdg_config_home}/revChatGPT/config.json")
        user_home = getenv("HOME")
        if user_home:
            config_files.append(f"{user_home}/.config/revChatGPT/config.json")

        config_file = next((f for f in config_files if exists(f)), None)
        if not config_file:
            raise Exception(
                "Please create and populate ./config.json, $XDG_CONFIG_HOME/revChatGPT/config.json, or ~/.config/revChatGPT/config.json to continue"
            )

        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)

        debug = True
        chatbot = None  # Chatbot(config, debug=debug, captcha_solver=CaptchaSolver())
        '''
        if prompt.startswith("!"):
            if prompt == "!help":
                return(
                    """
                !help - Show this message
                !reset - Forget the current conversation
                !refresh - Refresh the session authentication
                !rollback - Rollback the conversation by 1 message
                !config - Show the current configuration
                !exit - Exit the program
                """,
                )
            elif prompt == "!reset":
                chatbot.reset_chat()
                return("Chat session reset.")
            elif prompt == "!refresh":
                chatbot.refresh_session()
                return("Session refreshed.\n")
            elif prompt == "!rollback":
                chatbot.rollback_conversation()
                return("Chat session rolled back.")
            elif prompt == "!config":
                return(json.dumps(config, indent=4))
        '''

        try:
            message = chatbot.get_chat_response(prompt)
            return str(message["message"])
        except Exception as exc:
            import traceback

            print(traceback.format_exc())
            return "Something went wrong!"
    except Exception as exc:
        return "Something went wrong! Please run with --debug to see the error."
