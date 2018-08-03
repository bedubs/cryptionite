import os

import wx


class EncryptPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.file = ""
        self.key = ""

        vbox = wx.BoxSizer(wx.VERTICAL)

        tbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        bbox = wx.BoxSizer(wx.VERTICAL)

        files = wx.StaticBox(self, -1, "File")
        file_box_sizer = wx.StaticBoxSizer(files, wx.VERTICAL)

        keys = wx.StaticBox(self, -1, "Key")
        key_box_sizer = wx.StaticBoxSizer(keys, wx.VERTICAL)

        file_box = wx.BoxSizer(wx.VERTICAL)
        key_box = wx.BoxSizer(wx.VERTICAL)

        self.ed_dropdown = wx.ComboBox(self, -1, choices=["Encrypt", "Decrypt"])
        self.file_btn = wx.Button(self, label="File")
        self.file_path = wx.TextCtrl(self, style=wx.TE_READONLY)

        tbox.Add(wx.StaticText(self, -1, label="Choose: "), 0, wx.ALIGN_RIGHT, 5)
        tbox.Add(self.ed_dropdown, 1, wx.EXPAND | wx.ALL, 10)

        file_box.Add(self.file_btn, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        file_box.Add(self.file_path, 1, wx.EXPAND | wx.ALL, 5)
        file_box_sizer.Add(file_box, 1, wx.EXPAND | wx.ALL, 10)

        self.keyfile_chk = wx.CheckBox(self, -1)
        self.keyfile_btn = wx.Button(self, label="Key File")
        self.keyfile_path = wx.TextCtrl(self, style=wx.TE_READONLY)

        self.keyfile_btn.Enable(False)
        self.keyfile_path.Enable(False)

        self.key_passwd = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.keyfile_create = wx.CheckBox(self, -1)

        key_box.Add(self.keyfile_chk, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        key_box.Add(wx.StaticText(self, label="Do you have a local key file? "), 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        key_box.Add(self.keyfile_btn, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        key_box.Add(self.keyfile_path, 1, wx.ALL | wx.EXPAND, 5)
        key_box.Add(wx.StaticText(self, label="Password: "), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        key_box.Add(self.key_passwd, 1, wx.ALL | wx.EXPAND, 5)
        key_box.Add(wx.StaticText(self, label="Create local key file? "), 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        key_box.Add(self.keyfile_create, 0, wx.ALL | wx.EXPAND, 5)
        key_box_sizer.Add(key_box, 1, wx.ALL | wx.EXPAND, 10)

        hbox.Add(file_box_sizer, 1, wx.ALL | wx.LEFT, 10)
        hbox.Add(key_box_sizer, 1, wx.ALL | wx.LEFT, 10)

        self.aes_path = wx.StaticText(self, label="")
        self.ok_btn = wx.Button(self, label="Ok")

        encrypt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        encrypt_sizer.Add(self.ok_btn, 0, wx.ALIGN_RIGHT)

        bbox.Add(self.aes_path, 1, wx.ALL | wx.CENTER, 5)
        bbox.Add(encrypt_sizer, 1, wx.ALL | wx.CENTER, 5)

        vbox.Add(tbox, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(bbox, 1, wx.ALL | wx.CENTER, 10)

        self.file_btn.Bind(wx.EVT_BUTTON, self.open_file_dialog)
        self.keyfile_btn.Bind(wx.EVT_BUTTON, self.open_keyfile_dialog)
        self.keyfile_chk.Bind(wx.EVT_CHECKBOX, self.toggle_key_controls)

        self.ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)

        self.SetSizer(vbox)
        self.Centre()
        self.Fit()

    def toggle_file_controls(self, event):
        local_file = event.GetEventObject().GetValue()
        self.file_path.Enable(local_file)

    def toggle_key_controls(self, event):
        local_key = event.GetEventObject().GetValue()
        self.keyfile_btn.Enable(local_key)
        self.keyfile_path.Enable(local_key)
        self.key_passwd.Enable(not local_key)
        self.keyfile_create.Enable(not local_key)

    def open_file_dialog(self, event):
        file_type = "All files (*.*)|*.*"
        if self.ed_dropdown.GetSelection() == 1:
            file_type = "AES files (*.aes)|*.aes"
        file_dialog = wx.FileDialog(self, "Open", "", "", file_type, wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        file_dialog.ShowModal()
        self.file = file_dialog.GetPath()
        file_dialog.Destroy()
        self.file_path.SetValue(self.file)
        return

    def open_keyfile_dialog(self, event):
        file_type = "Key files (*.key)|*.key"
        file_dialog = wx.FileDialog(self, "Open", "", "", file_type, wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        file_dialog.ShowModal()
        self.key = file_dialog.GetPath()
        file_dialog.Destroy()
        self.keyfile_path.SetValue(self.key)
        self.key = self.read_keyfile(self.key)
        return

    def read_keyfile(self, key):
        with open(key) as keyfile:
            key_hash = keyfile.read()
        return key_hash

    def on_ok(self, event):
        if self.ed_dropdown.GetSelection() == 1:
            from cryption import decrypt
            new_file = os.path.basename(self.file)[0:-4]
            try:
                password = self.key
                if not self.keyfile_chk:
                    password = hash_passwd(self.key)
                new_file = decrypt(new_file, self.file, password)
            except ValueError as e:
                new_file = str(e)
        else:
            key_file = None
            if self.keyfile_create:
                key_dialog = wx.FileDialog(self, "Save", "", "", "Key file (*.key)|*.key", wx.FD_SAVE)
                key_dialog.ShowModal()
                key_file = key_dialog.GetPath()
                key_dialog.Destroy()
            from cryption import encrypt
            new_file = encrypt(self.file, hash_passwd(self.key, key_file=key_file))
        self.aes_path.SetLabel(new_file)
        self.file_path.SetValue("")
        self.key_passwd.SetValue("")


def hash_passwd(passwd, key_file=None):
    import hashlib
    hash = hashlib.sha512()
    hash.update(passwd.encode())
    if key_file:
        with open(key_file + ".key", "w") as key_file:
            key_file.write(hash.hexdigest())
    return hash.hexdigest()
