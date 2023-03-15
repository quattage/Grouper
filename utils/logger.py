import bpy

do_logs = True


class logger:

    def enable():
        logger.do_logs = True

    def disable():
        logger.do_logs = False

    def log(message, importance = ""):
        message = str(message)
        if do_logs:
            prefix = "\033[90m GROUPER MESSAGE: \033[3m \033[3m"
            if importance == "REGISTRY":
                prefix = "\033[92m GROUPER REGISTRY: \033[3m"
            elif importance == "DEBUG":
                prefix = " \033[93m GROUPER DEBUG: \033[3m"
            elif importance == "ERROR":
                prefix = "\033[91m GROUPER ERROR: \033[3m"
            reset = "\u001b[0m"
            header = "\033[93m >>>" + reset
            print(header, prefix + message + reset)
