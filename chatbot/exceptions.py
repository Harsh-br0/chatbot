class ChatBotException(Exception):
    pass


class LoaderNotSupported(ChatBotException):
    pass


class MimeTypeInvalid(ChatBotException):
    pass
