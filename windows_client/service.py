import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import asyncio
from main import WindowsClipboardClient
import logging

class UniversalClipboardService(win32serviceutil.ServiceFramework):
    _svc_name_ = "UniversalClipboard"
    _svc_display_name_ = "Universal Clipboard Service"
    _svc_description_ = "Syncs clipboard between Windows and Mac devices"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.client = None
        self.loop = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        if self.loop:
            self.loop.stop()
        if self.client:
            self.client.is_connected = False

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        logging.basicConfig(
            filename='C:\\ProgramData\\UniversalClipboard\\service.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            self.client = WindowsClipboardClient()
            self.loop.run_until_complete(self.client.connect())
            
            while True:
                if win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_OBJECT_0:
                    break
                
        except Exception as e:
            logging.error(f"Service error: {e}")
        finally:
            if self.loop:
                self.loop.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(UniversalClipboardService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(UniversalClipboardService) 