import sys
import threading
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QProgressBar
import ipaddress
from ping3 import ping

class WorkerSignals(QObject):
    progress = pyqtSignal(int)
    output = pyqtSignal(str)

class NetworkScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Enter the CIDR:"))
        self.cidr_input = QLineEdit()
        layout.addWidget(self.cidr_input)
        self.cidr_input.setText("192.168.1.0/24")
        self.scan_button = QPushButton("Scan Network")
        self.scan_button.clicked.connect(self.scan_network)
        layout.addWidget(self.scan_button)

        self.output = QTextEdit()
        layout.addWidget(self.output)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.setWindowTitle("Network Scanner")
        self.show()

    def scan_network(self):
        self.output.clear()
        cidr = self.cidr_input.text()

        try:
            network = ipaddress.ip_network(cidr, strict=False)
            subnet_24 = ipaddress.IPv4Network(f"{network.network_address}/24")
        except ValueError:
            self.output.append("Invalid CIDR.")
            return

        scanned_ips = 0
        total_ips = 255
        threads = []
        signals = WorkerSignals()
        signals.progress.connect(self.progress_bar.setValue)
        signals.output.connect(self.output.append)

        def scan_ip(ip):
            nonlocal scanned_ips
            response_time = ping(str(ip), timeout=2, unit="ms")

            if response_time is not None and response_time > 0.001:
                alive_host = f"{ip} is alive (RTT: {response_time:.2f} ms)"
                signals.output.emit(alive_host)

            scanned_ips += 1
            progress = int((scanned_ips / total_ips) * 100)  # Cast progress to integer
            signals.progress.emit(progress)

        def scan_thread():
            nonlocal threads
            for ip in subnet_24.hosts():
                t = threading.Thread(target=scan_ip, args=(ip,))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()
            print("Scan completed.")
            signals.progress.emit(100)

        main_thread = threading.Thread(target=scan_thread)
        main_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scanner = NetworkScanner()
    sys.exit(app.exec_())
