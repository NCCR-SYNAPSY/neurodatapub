# Copyright © 2021-2022 Connectomics Lab
# University Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland,
# and contributors
#
#  This software is distributed under the open-source license Apache 2.0.

"""`neurodatapub.utils.qt`: utils functions for Qt style sheets."""

import pkg_resources


def return_global_style_sheet():
    """
    Return the global Qt style sheet of the GUI.

    Returns
    -------
    style_sheet : str
        Qt style sheet
    """
    style_sheet = '''
        QLabel {
            font: 12pt "Verdana";
            margin-left: 5px;
            background-color: transparent;
        }
        QPushButton {
            background-color: #3D3D3D;
            border-style: outset;
            border: 2px solid #555555;
            border-radius: 4px;
            min-width: 20px;
            icon-size: 20px;
            font: bold 12pt "Verdana";
            margin: 10px;
            padding:6px 6px;
            color: #FFFFFF;
        }
        QPushButton:pressed {
            border-style: inset;
            color: #3D3D3D;
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #dadbde, stop: 1 #f6f7fa);
        }
        QPushButton:disabled {
            background-color: #878787;
            border-style: outset;
            border: 2px solid #989898;
            border-radius: 4px;
            min-width: 20px;
            icon-size: 20px;
            font: bold 12pt "Verdana";
            margin: 10px;
            padding:5px 5px;
            color: #a9a9a9;
        }

        QMainWindow {
            background-color: #dadbde;
        }
        QMainWindow::separator {
            background: #dadbde;
            width: 1px; /* when vertical */
            height: 1px; /* when horizontal */
        }
        QMainWindow::separator:hover {
            background: red;
        }

        QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid #dadbde;
        }

        QTabWidget::tab-bar {
            left: 5px; /* move to the right by 5px */
        }

        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QTabBar {
            font: bold 12pt "Verdana";
        }

        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QTabBar::tab {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                        stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
            border: 2px solid #C4C4C3;
            border-bottom-color: #dadbde; /* same as the pane color */
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            padding: 6px;
        }

        QTabBar::tab:selected, QTabBar::tab:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                        stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
        }

        QTabBar::tab:selected {
            border-color: #9B9B9B;
            border-bottom-color: #dadbde; /* same as pane color */
        }

        QTabBar::tab:!selected {
            margin-top: 2px; /* make non-selected tabs look smaller */
        }

        /* make use of negative margins for overlapping tabs */
        QTabBar::tab:selected {
            /* expand/overlap to the left and right by 4px */
            margin-left: -4px;
            margin-right: -4px;
        }

        QTabBar::tab:first:selected {
            margin-left: 0; /* the first selected tab has nothing to overlap with on the left */
        }

        QTabBar::tab:last:selected {
            margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
        }

        QTabBar::tab:only-one {
            margin: 0; /* if there is only one tab, we don't want overlapping margins */
        }
        '''
    return style_sheet


def return_folder_button_style_sheet():
    """
    Return the Qt style sheet for the traitsui `FileEditor` and `DirectoryEditor`.

    Returns
    -------
    style_sheet_folder_button : str
        Qt style sheet
    """
    style_sheet_folder_button = '''
        QLabel {
            font: 12pt "Verdana";
            margin-left: 5px;
            background-color: transparent;
        }
        QPushButton {
            border: 0px solid lightgray;
            border-radius: 4px;
            color: transparent;
            background-color: transparent;
            min-width: 20px;
            icon-size: 20px;
            font: 12pt "Verdana";
            margin: 10px;
            padding: 6px;
        }
        QPushButton:pressed {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #dadbde, stop: 1 #f6f7fa);
        }
        '''
    return style_sheet_folder_button


def return_save_json_button_style_sheet():
    """
    Return the Qt style sheet for the button that saves JSON configuration files.

    Returns
    -------
    style_sheet_save_json_button : str
        Qt style sheet
    """
    save_json_icon = pkg_resources.resource_filename(
            'neurodatapub', "resources/save_json_icon_50x50.png"
    )
    save_json_icon_pressed = pkg_resources.resource_filename(
            'neurodatapub', "resources/save_json_icon_50x50_pressed.png"
    )
    style_sheet_save_json_button = '''
        QPushButton {{
            color: transparent;
            background-color: transparent;
            border-image: url({image}) 3 3 3 3;
            border-top: 3px transparent;
            border-bottom: 3px transparent;
            border-right: 3px transparent;
            border-left: 3px transparent;
            min-width: 20px;
            width: 50px;
            height: 50px;
        }}
        QPushButton:pressed {{
            border-image: url({image_pressed}) 3 3 3 3;
        }}
        '''
    return style_sheet_save_json_button.format(
        image=save_json_icon,
        image_pressed=save_json_icon_pressed
    )
