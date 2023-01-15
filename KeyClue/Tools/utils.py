class display_utils:
    send_buf = ""

    def display_print(self, message):
        display_utils.send_buf += message + "\n"

    def flush(self):
        buff_2 = display_utils.send_buf
        display_utils.send_buf = ""
        return buff_2
    