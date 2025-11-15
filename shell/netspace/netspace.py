from email.header import Header
import subprocess
import pam
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QItemDelegate, QListView, QListWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QGraphicsView, QSizePolicy, QMessageBox
import pwd, os
from PySide6 import QtCore, QtGui, QtWidgets
import requests

icon = QtGui.QIcon("/usr/share/icons/Adwaita/symbolic/devices/computer-symbolic.svg")
FileIcon = QtGui.QIcon("/usr/share/icons/Adwaita/symbolic/mimetypes/text-x-generic-symbolic.svg")
FolderIcon = QtGui.QIcon("/usr/share/icons/Adwaita/symbolic/places/folder-symbolic.svg")
ShareIcon = QtGui.QIcon("/usr/share/icons/Adwaita/symbolic/places/folder-publicshare-symbolic.svg")

def SearchNetworkForDevices():
    devices = []
    try:
        response = requests.get("http://localhost:1526/info").json()
        if response["isNetSpace"]:
            devices.append(response)
    except:
        pass
    return devices

def getShares(device):
    try:
        response = requests.get(f"http://{device['hostname']}:1526/cap/fileshare", timeout=2).json()
        return response.get('exposedShares', [])
    except Exception as e:
        print("Failed to get shares:", e)
        return []

def getShareFiles(device, share):
    if not share:
        return []
    try:
        response = requests.get(f"http://{device['hostname']}:1526/cap/fileshare/share/{share['slug']}/files", timeout=2).json()
        return response.get('files', [])
    except Exception as e:
        print("Failed to get share files:", e)
        return []

class DevicesModel(QtCore.QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.devices = SearchNetworkForDevices()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.devices)

    def reload(self):
        self.devices = SearchNetworkForDevices()
        self.layoutChanged.emit()

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.devices[index.row()]['hostname']
        if role == QtCore.Qt.ItemDataRole.DecorationRole:
            return icon
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return self.devices[index.row()]
        return None

class SharesModel(QtCore.QAbstractListModel):
    def __init__(self, device):
        super().__init__()
        shares = getShares(device)
        self.shares = shares if shares else []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.shares)

    def data(self, index, role):
        if not self.shares or index.row() >= len(self.shares):
            return None
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.shares[index.row()]['name']
        if role == QtCore.Qt.ItemDataRole.DecorationRole:
            return ShareIcon
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return self.shares[index.row()]
        return None

def uploadFile(device, share, file):
    try:
        response = requests.post(f"http://{device['hostname']}:1526/cap/fileshare/share/{share['slug']}/upload", files={"file": file})
        return response.json()
    except Exception as e:
        print("Failed to upload file:", e)
        return None

class FilesModel(QtCore.QAbstractListModel):
    def __init__(self, device, share):
        super().__init__()
        self.device = device
        self.share = share
        files = getShareFiles(device, share)
        self.files = files if files else []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.files)

    def data(self, index, role):
        if not self.files or index.row() >= len(self.files):
            return None
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.files[index.row()]['name']
        if role == QtCore.Qt.ItemDataRole.DecorationRole:
            if self.files[index.row()]['isDir']:
                return FolderIcon
            return FileIcon
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return self.files[index.row()]
        return None

    def uploadFile(self, file):
        return uploadFile(self.device, self.share, file)

    def reload(self):
        self.files = getShareFiles(self.device, self.share)
        self.layoutChanged.emit()

class FileShareWindow(QWidget):
    def __init__(self, device):
        super().__init__()
        self.device = device
        self.shares = SharesModel(device)
        self.share = None
        self.files = FilesModel(device, self.share)
        self.filesBrowser = QListView()
        self.filesBrowser.setAcceptDrops(True)
        self.filesBrowser.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.filesBrowser.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        
        self.setWindowTitle("Theta NetSpace File Browser - " + device['hostname'])
        self.setAcceptDrops(True)

        layout = QVBoxLayout()

        layout.setSpacing(13)

        headerRow = QHBoxLayout()
        headerRow.setAlignment(Qt.AlignmentFlag.AlignLeft)
        headerRow.setSpacing(10)
        layout.addLayout(headerRow)

        label = QLabel("Browsing Shares On: " + device['hostname'])
        label.setStyleSheet("font-size: 20px;")
        headerRow.addWidget(label)

        mainRow = QHBoxLayout()
        mainRow.setAlignment(Qt.AlignmentFlag.AlignLeft)
        mainRow.setSpacing(10)
        layout.addLayout(mainRow)

        sharesSidebar = QListView()
        sharesSidebar.setStyleSheet("max-width: 275px; background-color: #ffffff;")
        sharesSidebar.setModel(self.shares)
        mainRow.addWidget(sharesSidebar)

        sharesSidebar.selectionModel().selectionChanged.connect(
            lambda selected, deselected: self.shareSelected(selected, deselected)
        )

        self.filesBrowser.setStyleSheet("background-color: #ffffff;")
        self.filesBrowser.setModel(self.files)
        mainRow.addWidget(self.filesBrowser)

        self.setLayout(layout)
        self.show()
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event):
        if not self.share:
            QMessageBox.warning(self, "No Share Selected", "Please select a share first")
            return
            
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    try:
                        with open(file_path, 'rb') as f:
                            file_name = os.path.basename(file_path)
                            response = uploadFile(self.device, self.share, (file_name, f, 'application/octet-stream'))
                            if response:
                                QMessageBox.information(self, "Upload Successful", f"Successfully uploaded {file_name}")
                                # Refresh the file list
                                if hasattr(self, 'files') and hasattr(self.files, 'reload'):
                                    self.files.reload()
                                    self.filesBrowser.setModel(self.files)
                            else:
                                QMessageBox.warning(self, "Upload Failed", f"Failed to upload {file_name}")
                    except Exception as e:
                        QMessageBox.critical(self, "Upload Error", f"Error uploading {file_path}: {str(e)}")
        else:
            event.ignore()

    def shareSelected(self, selected, deselected):
        if selected.indexes():
            self.share = selected.indexes()[0].data(QtCore.Qt.ItemDataRole.UserRole)
            self.files = FilesModel(self.device, self.share)
            self.filesBrowser.setModel(self.files)


class main():
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setFixedWidth(800)
        self.window.setFixedHeight(600)
        self.window.setWindowTitle("Theta NetSpace")
        self.devicemodel = DevicesModel()

        self.thisDeviceLabel = QLabel("This Device")
        self.thisDeviceSubLabel = QLabel("Localhost")

        headerRow = QHBoxLayout()
        headerRow.setAlignment(Qt.AlignmentFlag.AlignLeft)
        headerRow.setSpacing(10)

        headerStartRow = QHBoxLayout()
        headerStartRow.setAlignment(Qt.AlignmentFlag.AlignLeft)
        headerStartRow.setSpacing(10)
        headerRow.addLayout(headerStartRow)

        label = QLabel("Connect To A NetSpace")
        label.setAlignment(Qt.AlignmentFlag.AlignLeading)
        label.setStyleSheet("font-size: 24px;")
        label.setContentsMargins(0, 0, 0, 0)
        label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        headerStartRow.addWidget(label)

        headerEndRow = QHBoxLayout()
        headerEndRow.setAlignment(Qt.AlignmentFlag.AlignRight)
        headerEndRow.setSpacing(10)
        headerEndRow.addStretch(1)
        headerRow.addLayout(headerEndRow)

        refreshButton = QPushButton("Refresh")
        refreshButton.clicked.connect(self.devicemodel.reload)
        headerEndRow.addWidget(refreshButton)

        layout = QVBoxLayout()
        layout.stretch(1)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)
        layout.addLayout(headerRow)

        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hlayout.setSpacing(20)
        layout.addLayout(hlayout)

        # store sidebar on self
        self.sidebar = QListView()
        self.sidebar.setModel(self.devicemodel)
        self.sidebar.setStyleSheet("max-width: 275px; background-color: #ffffff;")
        self.sidebar.selectionModel().selectionChanged.connect(
            lambda selected, deselected: self.selectionChanged(selected, deselected)
        )
        hlayout.addWidget(self.sidebar)

        thisDeviceSection = QVBoxLayout()
        thisDeviceSection.setAlignment(Qt.AlignmentFlag.AlignTop)
        hlayout.addLayout(thisDeviceSection)

        titlehlayout = QHBoxLayout()
        titlehlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        titlehlayout.setSpacing(10)
        thisDeviceSection.addLayout(titlehlayout)

        # OPEN BUTTON — now works
        openButton = QPushButton("Open")
        openButton.clicked.connect(self.openFileShareWindow)
        thisDeviceSection.addWidget(openButton)

        titleIcon = QLabel()
        titleIcon.setPixmap(QtGui.QPixmap("/usr/share/icons/Adwaita/scalable/devices/computer.svg").scaled(34, 34))
        titlehlayout.addWidget(titleIcon)

        titlevlayout = QVBoxLayout()
        titlevlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        titlevlayout.setSpacing(0)
        titlehlayout.addLayout(titlevlayout)

        self.thisDeviceLabel.setStyleSheet("font-size: 24px;")
        titlevlayout.addWidget(self.thisDeviceLabel)
        self.thisDeviceSubLabel.setStyleSheet("font-size: 12px;")
        titlevlayout.addWidget(self.thisDeviceSubLabel)

        self.window.setLayout(layout)
        self.window.show()
        self.app.exec()

    def selectionChanged(self, selected, deselected):
        self.thisDeviceLabel.setText(selected.indexes()[0].data(QtCore.Qt.ItemDataRole.DisplayRole))
        device = selected.indexes()[0].data(QtCore.Qt.ItemDataRole.UserRole)
        self.thisDeviceSubLabel.setText(device['network']['foundOn'])

    def openFileShareWindow(self):
        if not self.sidebar.selectedIndexes():
            return
        index = self.sidebar.selectedIndexes()[0]
        device = index.data(QtCore.Qt.ItemDataRole.UserRole)

        # keep reference alive
        self.fileWindow = FileShareWindow(device)


if __name__ == "__main__":
    main()

