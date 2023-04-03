#############################################################################
# zlib License
#
# (C) 2023 Cristóvão Beirão da Cruz e Silva <cbeiraod@cern.ch>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#############################################################################

from __future__ import annotations

from .base_gui import Base_GUI

import tkinter as tk
import tkinter.ttk as ttk  # For themed widgets (gives a more native visual to the elements)
import logging

import importlib.resources
from PIL import ImageTk, Image

class ETROC1_GUI(Base_GUI):
    def __init__(self, root: tk.Tk, logger: logging.Logger):
        super().__init__("ETROC1 I2C GUI", root, logger)

        self._valid_i2c_address = False

    def _about_contents(self, element: tk.Tk, column: int, row: int):
        self._about_img = ImageTk.PhotoImage(Image.open(importlib.resources.open_binary("i2c_gui.static", "ETROC1.png")))
        self._about_img_label = tk.Label(element, image = self._about_img)
        self._about_img_label.grid(column=column, row=row, sticky='')
        element.rowconfigure(row, weight=1)

        self._about_info_label = tk.Label(element, justify=tk.LEFT, wraplength=450, text="The ETROC1 I2C GUI was developed to read and write I2C registers from a connected ETROC1 device using a USB-ISS serial adapter. The code was developed and tested using a FSxx board and during a testbeam with an ETROC1 telescope")
        self._about_info_label.grid(column=column, row=row + 100, sticky='')

    def _fill_notebook(self):
        from .chips import ETROC1_Chip
        self._chip = ETROC1_Chip(parent=self, i2c_controller=self._i2c_controller)

        self._full_chip_display(self._chip)

    def _connection_update(self, value):
        super()._connection_update(value)

    def extra_global_controls(self, element: tk.Tk, column: int, row: int):
        self._frame_extra_global = ttk.Frame(element)
        self._frame_extra_global.grid(column=column, row=row, sticky=(tk.W, tk.E))

        self._extra_i2c_label = ttk.Label(self._frame_extra_global, text="I2C Address:")
        self._extra_i2c_label.grid(column=100, row=100)

    def read_all(self):
        if self._valid_i2c_address:
            self.send_message("Reading full ETROC1 chip")
            self._chip.read_all()
        else:
            self.send_message("Unable to read full ETROC1 chip")
        pass

    def write_all(self):
        if self._valid_i2c_address:
            self.send_message("Writing full ETROC1 chip")
            self._chip.write_all()
        else:
            self.send_message("Unable to write full ETROC1 chip")
        pass