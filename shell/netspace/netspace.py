from email.header import Header
import subprocess
import pam
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QItemDelegate, QListView, QListWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QGraphicsView, QSizePolicy, QMessageBox, QDialog, QDialogButtonBox
import pwd, os
from PySide6 import QtCore, QtGui, QtWidgets
import requests
import json
import os

icon = QtGui.QIcon("/usr/share/icons/Adwaita/symbolic/devices/computer-symbolic.svg")
FileIcon = QtGui.QIcon("/usr/share/icons/Adwaita/symbolic/mimetypes/text-x-generic-symbolic.svg")
FolderIcon = QtGui.QIcon("/usr/share/icons/Adwaita/symbolic/places/folder-symbolic.svg")
ShareIcon = QtGui.QIcon("/usr/share/icons/Adwaita/symbolic/places/folder-publicshare-symbolic.svg")

def SearchNetworkForDevices():
    devices = []
    # Check localhost first
    try:
        response = requests.get("http://localhost:1526/info").json()
        if response.get("isNetSpace"):
            devices.append({
                'hostname': 'localhost',
                'name': 'This Computer',
                'ip': '127.0.0.1'
            })
    except:
        pass
    
    # Check saved hosts
    try:
        hosts_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hosts.json')
        if os.path.exists(hosts_file):
            with open(hosts_file, 'r') as f:
                saved_hosts = json.load(f).get('hosts', [])
                for host in saved_hosts:
                    try:
                        response = requests.get(f"http://{host}:1526/info", timeout=2).json()
                        if response.get("isNetSpace"):
                            devices.append({
                                'hostname': host,
                                'name': response.get('name', f'Device at {host}'),
                                'ip': host
                            })
                    except:
                        continue
    except Exception as e:
        print(f"Error checking saved hosts: {e}")
    
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

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemNeverHasChildren

    def data(self, index, role):
        if not self.files or not index.isValid() or index.row() >= len(self.files):
            return None
            
        item = self.files[index.row()]
        if not item:
            return None
            
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return item.get('name', '')
            
        if role == QtCore.Qt.ItemDataRole.DecorationRole:
            return FolderIcon if item.get('isDir', False) else FileIcon
            
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return item
            
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
        self.filesBrowser.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.filesBrowser.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.filesBrowser.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        # Add download button
        self.downloadButton = QPushButton("Download Selected")
        self.downloadButton.clicked.connect(self.downloadSelectedFile)
        self.downloadButton.setEnabled(False)
        self.downloadButton.setVisible(True)  # Ensure button is always visible
        
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
        
        # Add download button to layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.downloadButton)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)

        # Configure the view for selection
        self.filesBrowser.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.filesBrowser.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.filesBrowser.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        # Configure the view for selection first
        self.filesBrowser.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.filesBrowser.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.filesBrowser.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        # Ensure model is properly set and connected
        if not self.files.rowCount():
            print("Warning: No files in model")
            
        # Connect selection model after everything is set up
        selection_model = self.filesBrowser.selectionModel()
        if selection_model:
            # Disconnect any existing connections to avoid duplicates
            try:
                selection_model.selectionChanged.disconnect()
            except:
                pass
            selection_model.selectionChanged.connect(self.handleSelectionChanged)
            print("Connected selection model:", selection_model)
            
            # Force an initial selection if there are items
            if self.files.rowCount() > 0:
                first_index = self.files.index(0, 0, QtCore.QModelIndex())
                if first_index.isValid():
                    selection_model.select(first_index, QtCore.QItemSelectionModel.Select)
        else:
            print("Warning: No selection model available")
        
        # Set initial button state
        self.updateButtonState()
        
        # Debug: Print model and view info
        print("Files model:", self.files)
        print("Files model row count:", self.files.rowCount())
        print("View:", self.filesBrowser)
        print("View model:", self.filesBrowser.model())
        print("View selection mode:", self.filesBrowser.selectionMode())
        print("View selection behavior:", self.filesBrowser.selectionBehavior())

        self.setLayout(layout)
        self.show()
        
    def shareSelected(self, selected, deselected):
        """Handle when a share is selected in the sidebar"""
        indexes = selected.indexes()
        if not indexes:
            return
            
        index = indexes[0]
        share_info = index.data(QtCore.Qt.ItemDataRole.UserRole)
        if not share_info:
            return
            
        self.share = share_info
        print(f"Selected share: {share_info['name']}")
        
        # Update the files model with the selected share
        self.files = FilesModel(self.device, share_info)
        self.filesBrowser.setModel(self.files)
        
        # Reconnect selection handler for the files view
        selection_model = self.filesBrowser.selectionModel()
        if selection_model:
            try:
                selection_model.selectionChanged.disconnect()
            except:
                pass
            selection_model.selectionChanged.connect(self.handleSelectionChanged)
            print("Reconnected selection model after share change")
        
        # Update button state
        self.updateButtonState()
        
        # Debug info
        print(f"Files in share '{share_info['name']}': {self.files.rowCount()}")

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

    def handleSelectionChanged(self, selected, deselected):
        print("\n=== Selection Changed ===")
        print("Selected indexes:", selected.indexes())
        print("Deselected indexes:", deselected.indexes())
        
        # Force update the button state immediately
        self.updateButtonState()
        
        # Process events to ensure UI updates
        QApplication.processEvents()
        
    def updateButtonState(self):
        # Get selection directly from the view
        selected = self.filesBrowser.selectedIndexes()
        has_selection = len(selected) > 0
        
        print("\n--- Update Button State ---")
        print(f"Selected indexes count: {len(selected)}")
        print(f"Has selection: {has_selection}")
        
        if has_selection:
            for i, idx in enumerate(selected):
                print(f"  Item {i} data: {idx.data(QtCore.Qt.ItemDataRole.UserRole)}")
                print(f"  Item {i} display: {idx.data(QtCore.Qt.ItemDataRole.DisplayRole)}")
        
        # Update button state
        self.downloadButton.setEnabled(has_selection)
        self.downloadButton.repaint()  # Force repaint to update the button state
        print(f"Button enabled: {self.downloadButton.isEnabled()}")
        
        # Print debug info about the button
        print(f"Button object: {self.downloadButton}")
        print(f"Button is enabled: {self.downloadButton.isEnabled()}")
        print(f"Button is visible: {self.downloadButton.isVisible()}")

    def downloadSelectedFile(self):
        selected = self.filesBrowser.selectedIndexes()
        print("Download clicked - Selected indexes:", selected)
        if not selected:
            print("No file selected")
            return
            
        file_info = selected[0].data(QtCore.Qt.ItemDataRole.UserRole)
        print("File info:", file_info)
        if not file_info:
            return
            
        # Open file dialog to choose download location
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save File",
            file_info['name'],
            "All Files (*)"
        )
        
        if save_path:
            if downloadFile(self.device, self.share, file_info, save_path):
                print(f"Successfully downloaded {file_info['name']} to {save_path}")

def downloadFile(device, share, file, save_path):
    try:
        url = f"http://{device['hostname']}:1526/cap/fileshare/share/{share['slug']}/download?file={file['name']}"
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        print("Failed to download file:", e)
        return False

class main():
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setFixedWidth(800)
        self.window.setFixedHeight(600)
        self.window.setWindowTitle("Theta NetSpace")
        self.devicemodel = DevicesModel()
        
        # Load saved hosts
        self.hosts_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hosts.json')
        self.saved_hosts = self.load_hosts()

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
        
        # Add Host button
        self.addHostButton = QPushButton("Add Host")
        self.addHostButton.clicked.connect(self.show_add_host_dialog)
        headerEndRow.addWidget(self.addHostButton)

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
    
    def load_hosts(self):
        try:
            if os.path.exists(self.hosts_file):
                with open(self.hosts_file, 'r') as f:
                    data = json.load(f)
                    return data.get('hosts', [])
        except Exception as e:
            print(f"Error loading hosts: {e}")
        return []
    
    def save_hosts(self):
        try:
            with open(self.hosts_file, 'w') as f:
                json.dump({'hosts': self.saved_hosts}, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving hosts: {e}")
            return False
    
    def show_add_host_dialog(self):
        dialog = QDialog(self.window)
        dialog.setWindowTitle("Add New Host")
        dialog.setFixedWidth(400)
        
        layout = QVBoxLayout()
        
        # IP Address Input
        ip_layout = QHBoxLayout()
        ip_label = QLabel("IP Address:")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.100")
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.add_host(dialog))
        button_box.rejected.connect(dialog.reject)
        
        # Add widgets to layout
        layout.addLayout(ip_layout)
        layout.addWidget(QLabel("Note: Port 1526 will be used for the connection"))
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def add_host(self, dialog):
        ip = self.ip_input.text().strip()
        if not ip:
            QMessageBox.warning(dialog, "Error", "Please enter an IP address")
            return
            
        # Basic IP validation
        try:
            parts = ip.split('.')
            if len(parts) != 4 or not all(0 <= int(part) <= 255 for part in parts):
                raise ValueError
        except (ValueError, AttributeError):
            QMessageBox.warning(dialog, "Error", "Please enter a valid IP address")
            return
            
        # Check for duplicates
        if ip in self.saved_hosts:
            QMessageBox.information(dialog, "Info", "This host is already in the list")
            return
            
        # Add to saved hosts and update the model
        self.saved_hosts.append(ip)
        if self.save_hosts():
            self.devicemodel.reload()
            dialog.accept()
        else:
            QMessageBox.critical(dialog, "Error", "Failed to save host")
    
    def remove_host(self, ip):
        if ip in self.saved_hosts:
            self.saved_hosts.remove(ip)
            if self.save_hosts():
                self.devicemodel.reload()
            else:
                QMessageBox.critical(self.window, "Error", "Failed to remove host")
        else:
            QMessageBox.information(self.window, "Info", "Host not found")
    
    def selectionChanged(self, selected, deselected):
        indexes = selected.indexes()
        if not indexes:
            return
            
        index = indexes[0]
        if index.isValid():
            device = self.devicemodel.devices[index.row()]
            self.openFileShareWindow(device)
    
    def openFileShareWindow(self, device=None):
        if device is None:
            # Create a dummy device for localhost
            device = {
                'hostname': 'localhost',
                'name': 'This Computer',
                'ip': '127.0.0.1'
            }
        self.window = FileShareWindow(device)

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

