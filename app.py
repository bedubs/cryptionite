import wx
from encrypt_panel import EncryptPanel


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(1200, 520))
        self.SetBackgroundColour("lightgray")

        self.panel = EncryptPanel(self)

        self.SetDefaultItem(self.panel.ok_btn)

        self.Show(True)


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None, "Cryptionite")
    app.MainLoop()
