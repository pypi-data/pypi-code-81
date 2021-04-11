from pathlib import Path

from .mainwindow import Ui_MainWindow
from Qt.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QShortcut,
    QSizePolicy,
    QSpacerItem,
    QStyle,
    QVBoxLayout,
)
from Qt.QtGui import QMovie, QKeySequence
from Qt.QtCore import QSize
from Qt.QtCore import Qt as QtCoreQt


class MultiGifView(QMainWindow, Ui_MainWindow):
    """A program for viewing .gif files"""

    def __init__(self, filenames, *, max_columns, titles):
        super().__init__(None)
        self.setupUi(self)

        # extra keyboard shortcuts
        quit_shortcut = QShortcut(QKeySequence("Q"), self)
        quit_shortcut.activated.connect(QApplication.instance().quit)
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(QApplication.instance().quit)
        quit_shortcut = QShortcut(QKeySequence("Ctrl+X"), self)
        quit_shortcut.activated.connect(QApplication.instance().quit)
        quit_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        quit_shortcut.activated.connect(QApplication.instance().quit)
        previous_shortcut = QShortcut(QKeySequence("left"), self)
        previous_shortcut.activated.connect(self.previous_action)
        next_shortcut = QShortcut(QKeySequence("right"), self)
        next_shortcut.activated.connect(self.next_action)
        beginning_shortcut = QShortcut(QKeySequence("up"), self)
        beginning_shortcut.activated.connect(self.beginning_action)
        end_shortcut = QShortcut(QKeySequence("down"), self)
        end_shortcut.activated.connect(self.end_action)

        def set_clicked(widget, function):
            widget.clicked.connect(function)
            if hasattr(function, "__doc__"):
                widget.setToolTip(function.__doc__.strip())

        set_clicked(self.play_button, self.play_action)
        set_clicked(self.previous_button, self.previous_action)
        set_clicked(self.next_button, self.next_action)
        set_clicked(self.beginning_button, self.beginning_action)
        set_clicked(self.end_button, self.end_action)

        set_clicked(self.quit_button, self.quit_action)

        set_clicked(self.zoom_out_button, self.zoom_out_action)
        set_clicked(self.zoom_in_button, self.zoom_in_action)
        set_clicked(self.zoom_reset_button, self.zoom_reset_action)
        self.zoom_box.editingFinished.connect(self.zoom_changed_action)
        self.zoom_box.setToolTip(self.zoom_changed_action.__doc__.strip())

        self.zoom = 100.0

        if max_columns < 1:
            raise ValueError(f"Number of columns must be positive, got {max_columns}")
        n_columns = min(max_columns, len(filenames))
        self.columns = [self.column0]
        for i in range(n_columns)[1:]:
            # Create column
            column = QVBoxLayout()
            column.setObjectName(f"column{i}")
            spacerItem = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
            column.addItem(spacerItem)
            self.gif_layout.addLayout(column)
            self.columns.append(column)

        self.extra_movies = []
        self.extra_gif_widgets = []
        for i, arg in enumerate(filenames):
            gif_widget = QLabel(self.centralwidget)
            gif_widget.setText("")
            gif_widget.setToolTip(arg)
            gif_widget.setObjectName(f"gif_widget{i + 1}")

            filepath = Path(arg)
            movie = QMovie(str(filepath))
            movie.setCacheMode(QMovie.CacheAll)
            gif_widget.setMovie(movie)
            movie.jumpToFrame(0)
            movie.unscaled_width = movie.currentImage().width()
            movie.unscaled_height = movie.currentImage().height()

            column = self.columns[i % n_columns]
            position = column.count() - 1

            if titles:
                title_widget = QLabel(self.centralwidget)
                title_widget.setText(arg)
                title_widget.setAlignment(QtCoreQt.AlignCenter)
                title_widget.setObjectName(f"title_widget{i + 1}")

                column.insertWidget(position, title_widget)
                position = position + 1

            column.insertWidget(position, gif_widget)

            self.extra_movies.append(movie)
            self.extra_gif_widgets.append(gif_widget)

        # Set a sensible initial width
        (
            left_margin,
            top_margin,
            right_margin,
            bottom_margin,
        ) = self.verticalLayout_main.getContentsMargins()
        scrollable_width = (
            left_margin
            + sum([c.sizeHint().width() for c in self.columns])
            + self.columns[0].spacing()
            + sum([2 * c.spacing() for c in self.columns[1:-1]])
            + self.columns[-1].spacing()
            + self.scrollArea.verticalScrollBar().sizeHint().width()
            + right_margin
        )
        max_width = (
            QApplication.desktop().availableGeometry().width()
            - left_margin
            - right_margin
        )
        self.scrollArea.setMinimumWidth(min(scrollable_width, max_width))

        # Set a sensible initial height
        column_heights = [c.sizeHint().height() for c in self.columns]
        highest_col_index = column_heights.index(max(column_heights))
        scrollable_height = (
            top_margin
            + column_heights[highest_col_index]
            + self.columns[highest_col_index].spacing()
            + self.scrollArea.horizontalScrollBar().sizeHint().height()
            + bottom_margin
        )
        control_bar_height = (
            self.horizontalLayout.sizeHint().height()
            + 2 * self.horizontalLayout.spacing()
        )
        menu_bar_height = self.menubar.sizeHint().height()
        title_bar_height = QApplication.style().pixelMetric(QStyle.PM_TitleBarHeight)
        max_height = (
            QApplication.desktop().availableGeometry().height()
            - top_margin
            - bottom_margin
            - control_bar_height
            - menu_bar_height
            - title_bar_height
        )
        self.scrollArea.setMinimumHeight(min(scrollable_height, max_height))

        # want the longest-running gif to be the one that's directly controlled, so that
        # it can play all the way to the end, not have to stop when the first movie
        # reaches its last frame
        frame_counts = [m.frameCount() for m in self.extra_movies]
        ind_longest = frame_counts.index(max(frame_counts))
        self.movie = self.extra_movies.pop(ind_longest)

        # Create actions so extra movies follow self.movie
        self.movie.frameChanged.connect(self.change_frames)

    def play_action(self):
        """<html><head/><body><p><b>Play</b><br>
        space</p></body></html>
        """
        if self.movie.state() == QMovie.Running:
            self.movie.setPaused(True)
        elif self.movie.state() == QMovie.Paused:
            self.movie.setPaused(False)
        else:
            self.movie.start()

    def previous_action(self):
        """<html><head/><body><p><b>Back one frame</b><br>
        p, left</p></body></html>
        """
        self.movie.jumpToFrame(
            (self.movie.currentFrameNumber() - 1) % self.movie.frameCount()
        )

    def next_action(self):
        """<html><head/><body><p><b>Forward one frame</b><br>
        n, right</p></body></html>
        """
        self.movie.jumpToNextFrame()

    def beginning_action(self):
        """<html><head/><body><p><b>Back to beginning</b><br>
        b, up</p></body></html>
        """
        self.movie.jumpToFrame(0)

    def end_action(self):
        """<html><head/><body><p><b>Forward to end</b><br>
        e, down</p></body></html>
        """
        self.movie.jumpToFrame(self.movie.frameCount() - 1)

    def quit_action(self):
        """<html><head/><body><p><b>Quit</b><br>
        q, Ctrl-q, Ctrl-w, Ctrl-x</p></body></html>
        """
        QApplication.instance().quit

    def change_frames(self, new_frame):
        """Change all the frames in step"""
        for movie in self.extra_movies:
            length = movie.frameCount()
            if new_frame < length:
                movie.jumpToFrame(new_frame)
            else:
                movie.jumpToFrame(length - 1)

    def reset_minimum_size(self):
        """Allow window to be shrunk from default size"""
        self.scrollArea.setMinimumWidth(0)
        self.scrollArea.setMinimumHeight(0)

    def set_zoom(self, new_zoom):
        try:
            self.zoom = float(new_zoom)
        except ValueError:
            # Make the box red
            self.zoom_box.setStyleSheet("QLineEdit { background-color: #aa0000 }")
            return
        self.zoom_box.setStyleSheet("QLineEdit { background-color: #FFFFFF }")
        self.zoom_box.setText(str(int(round(self.zoom))))

        current_frame = self.movie.currentFrameNumber()
        scale_factor = self.zoom / 100.0

        self.movie.setScaledSize(
            QSize(
                scale_factor * self.movie.unscaled_width,
                scale_factor * self.movie.unscaled_height,
            )
        )
        for movie in self.extra_movies:
            movie.setScaledSize(
                QSize(
                    scale_factor * movie.unscaled_width,
                    scale_factor * movie.unscaled_height,
                )
            )

        # change frame to make the image re-draw
        self.movie.jumpToFrame(0 if current_frame > 0 else 1)
        self.movie.jumpToFrame(current_frame)

    def zoom_changed_action(self):
        """<html><head/><body><p><b>Set zoom factor</b></p></body></html>"""
        self.set_zoom(self.zoom_box.text())

    def zoom_out_action(self):
        """<html><head/><body><p><b>Zoom out</b><br>
        -</p></body></html>
        """
        new_zoom = 0.8 * self.zoom
        if self.zoom >= 100.0:
            # Round to nearest 10%
            new_zoom = round(new_zoom, -1)
        elif self.zoom > 20.0:
            # Round to nearest 5%
            new_zoom = round(2.0 * new_zoom, -1) / 2.0
        elif self.zoom > 5.0:
            # Round to nearest 1%
            new_zoom = round(new_zoom)
        elif self.zoom > 0.5:
            # Round to nearest 0.1%
            new_zoom = round(new_zoom, 1)
        elif self.zoom > 0.05:
            # Round to nearest 0.01%
            new_zoom = round(new_zoom, 2)

        self.set_zoom(new_zoom)

    def zoom_in_action(self):
        """<html><head/><body><p><b>Zoom in</b><br>
        +</p></body></html>
        """
        new_zoom = 1.25 * self.zoom
        if self.zoom >= 100.0:
            # Round to nearest 10%
            new_zoom = round(new_zoom, -1)
        elif self.zoom > 20.0:
            # Round to nearest 5%
            new_zoom = round(2.0 * new_zoom, -1) / 2.0
        elif self.zoom > 5.0:
            # Round to nearest 1%
            new_zoom = round(new_zoom)
        elif self.zoom > 0.5:
            # Round to nearest 0.1%
            new_zoom = round(new_zoom, 1)
        elif self.zoom > 0.05:
            # Round to nearest 0.01%
            new_zoom = round(new_zoom, 2)

        self.set_zoom(new_zoom)

    def zoom_reset_action(self):
        """<html><head/><body><p><b>Reset original size</b><br>
        =</p></body></html>
        """
        self.set_zoom(100.0)
