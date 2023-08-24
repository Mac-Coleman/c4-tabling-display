from abc import ABC, abstractmethod

from textual.message import Message

class BackgroundBase(ABC):
    """
    An abstract base class for backgrounds to extend from.
    This defines a common interface that backgrounds can use.

    Your custom background must extend this BackgroundBase class, as well as one of the
    textual widget classes, such as textual.widgets.Static or textual.widget.Widget

    Additionally, your custom background must have a class variable named 'DEFAULT_CSS' which contains a string
    with the default CSS for your background widget. For an example, see background_default.py.
    """

    class BackgroundEnded(Message):
        """
        The app uses this message to understand when the background has finished cleaning up.
        Post this message with self.post_message(self.BackgroundEnded()) when your background has finished cleaning up gracefully.
        If your background doesn't need to spend much time cleaning up, post the message inside of the stop() method after your cleanup code.
        """
        def __init__(self):
            super().__init__()

    @property
    @abstractmethod
    def author(self) -> str:
        """This method must return the name of the author of the background. Make this function return your name as a string."""
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        """This method must return the title of the background. Make this function return the title as a string."""
        pass

    @abstractmethod
    def start(self) -> None:
        """
        This method should contain the setup logic used to start your background.
        For example, here you could make the background gently fade in.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        The app calls this method after the background has been running for a certain amount of time.
        Make sure that this method cleans up all state for the background, or begins causing the background to be cleaned up.
        When the background has finished cleaning up, make sure to post the BackgroundEnded message.

        This is intended to allow the backgrounds to finish gracefully, i.e. by letting backgrounds fade in and out rather than
        jarringly cutting from one background to the next.
        """
        pass

if __name__ == "__main__":
    print(BackgroundBase.__class__)