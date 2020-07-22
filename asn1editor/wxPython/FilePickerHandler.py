import os
from typing import Callable, Optional

import wx


class FilePickerHandler:
    def __init__(self, file_dialog_factory: Callable, propagator: Optional[Callable], overwrite_question: bool = False):
        self.__file_dialog_factory = file_dialog_factory
        self.__propagator = propagator
        self.__overwrite_question = overwrite_question
        self.filename = None

    # noinspection PyUnusedLocal
    def on_menu_click(self, e: wx.Event):
        del e
        with self.__file_dialog_factory() as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            filename = file_dialog.GetPath()
            self.file_selected(filename, file_dialog.GetParent())

    def file_selected(self, filename: Optional[str], window: wx.Window):
        if filename is not None:
            use_filename = True
            if self.__overwrite_question and os.path.exists(filename):
                use_filename = False
                with wx.MessageDialog(window, f'File {os.path.basename(filename)} already exists.\n\nDo you want to replace it?',
                                      style=wx.YES | wx.NO | wx.NO_DEFAULT | wx.ICON_WARNING) as question_dialog:
                    if question_dialog.ShowModal() == wx.ID_YES:
                        use_filename = True

            if use_filename:
                self.filename = filename
                if self.__propagator is not None:
                    self.__propagator(filename)
