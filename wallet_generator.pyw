"""
Name: Wallet Generator
Description: 
Author: Belp2801
Created: 09.11.2024
"""

import customtkinter
from CTkMessagebox import CTkMessagebox
import sys, os, csv, datetime

import bip32utils
from eth_account import Account
from mnemonic import Mnemonic

import base58
from solders.keypair import Keypair

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

os.chdir(os.path.dirname(os.path.realpath(__file__)))


class WalletGenerator(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wallet Generator")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.init_constants()
        self.init_vars()
        self.init_ctk_vars()

        self.build_widgets()

    # region init
    def init_constants(self):
        self.vm_dict = {'evm': "EVM", 'svm': "SVM"}
        self.type_dict = {1: "One Seed Phrase", 2: "Multi Seed Phrases"}
        self.mnemo = Mnemonic("english")

    def init_vars(self):
        self.wallets = []

    def init_ctk_vars(self):
        self.vm_var = customtkinter.StringVar()
        self.vm_var.set(list(self.vm_dict.keys())[0])
        self.type_var = customtkinter.StringVar()
        self.type_var.set(list(self.type_dict.keys())[0])
        self.combobox_vm_var = customtkinter.StringVar()
        self.combobox_text_var = customtkinter.StringVar()
        self.num_of_words_var = customtkinter.IntVar(value=12)
        self.num_of_wallets_var = customtkinter.IntVar(value=100)

    # endregion

    # region build ui
    def build_widgets(self):
        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

        self.build_input_frame()
        self.build_button_widget()
        self.build_footers()

    def build_input_frame(self):
        # VN
        vm_label = customtkinter.CTkLabel(self.input_frame, text="VM: ")
        def on_vm_combobox_select(event):
            for key, value in self.vm_dict.items():
                if value == self.combobox_vm_var.get():
                    self.vm_var.set(key)

        vm_entry = customtkinter.CTkOptionMenu(
            self.input_frame,
            state="readonly",
            values=list(self.vm_dict.values()),
            variable=self.combobox_vm_var,
            width=160,
            anchor="e",
            fg_color=["#F9F9FA", "#343638"],
            text_color=["#000", "#fff"],
            command=on_vm_combobox_select,
        )
        vm_entry.set(list(self.vm_dict.values())[0])
        vm_label.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=10)
        vm_entry.grid(
            row=0, column=1, columnspan=2, sticky="w", padx=(10, 10), pady=10
        )
        
        # Type
        type_label = customtkinter.CTkLabel(self.input_frame, text="Type: ")
        def on_type_combobox_select(event):
            for key, value in self.type_dict.items():
                if value == self.combobox_text_var.get():
                    self.type_var.set(key)

        type_entry = customtkinter.CTkOptionMenu(
            self.input_frame,
            state="readonly",
            values=list(self.type_dict.values()),
            variable=self.combobox_text_var,
            width=160,
            anchor="e",
            fg_color=["#F9F9FA", "#343638"],
            text_color=["#000", "#fff"],
            command=on_type_combobox_select,
        )

        type_label.grid(row=1, column=0, sticky="w", padx=(10, 0), pady=10)
        type_entry.grid(
            row=1, column=1, columnspan=2, sticky="w", padx=(10, 10), pady=10
        )

        type_entry.set(list(self.type_dict.values())[0])

        seed_num_label = customtkinter.CTkLabel(self.input_frame, text="Num of words: ")
        seed_num_entry = customtkinter.CTkOptionMenu(
            self.input_frame,
            state="readonly",
            values=["12", "15", "18", "24"],
            variable=self.num_of_words_var,
            anchor="e",
            width=160,
            fg_color=["#F9F9FA", "#343638"],
            text_color=["#000", "#fff"],
        )
        seed_num_entry.set("12")

        seed_num_label.grid(row=2, column=0, sticky="w", padx=(10, 0), pady=10)
        seed_num_entry.grid(
            row=2, column=1, columnspan=2, sticky="w", padx=(10, 10), pady=10
        )

        wallet_num_label = customtkinter.CTkLabel(
            self.input_frame, text="Num of wallets: "
        )
        wallet_num_entry = customtkinter.CTkComboBox(
            self.input_frame,
            values=["10", "100", "1000", "10000"],
            variable=self.num_of_wallets_var,
            justify="right",
            width=160,
            border_width=0,
        )

        wallet_num_entry.set("100")

        wallet_num_label.grid(row=3, column=0, sticky="w", padx=(10, 0), pady=10)
        wallet_num_entry.grid(row=3, column=1, sticky="w", padx=(10, 10), pady=10)

    def build_button_widget(self):
        button = customtkinter.CTkButton(
            self,
            text="Generate",
            command=self.run,
        )
        button.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="ew")

    def build_footers(self):
        cer = customtkinter.CTkLabel(self, text="@Powered by: Belp2801")
        cer.grid(row=4, column=0, columnspan=3, padx=10, pady=4)

    # endregion

    # region utils
    def generate_seed_phrases(self):
        return self.mnemo.generate(strength=int(128 / 12 * self.num_of_words_var.get()))

    def generate_evm_wallets(self, seed_phrase, num=1):
        for i in range(num):
            seed = self.mnemo.to_seed(seed_phrase)

            # Create BIP32 root_key
            root_key = bip32utils.BIP32Key.fromEntropy(seed)

            # Create child_key
            child_key = (
                root_key.ChildKey(44 + bip32utils.BIP32_HARDEN)
                .ChildKey(60 + bip32utils.BIP32_HARDEN)
                .ChildKey(0 + bip32utils.BIP32_HARDEN)
                .ChildKey(0)
                .ChildKey(i)
            )

            # Private key and address
            private_key = child_key.PrivateKey().hex()
            address = Account.from_key(private_key).address

            self.wallets.append(
                {
                    "seed_phrase": seed_phrase,
                    "address": address,
                    "private_key": private_key,
                }
            )
    
    def generate_svm_wallets(self, seed_phrase, num = 1):
        for i in range(num):
            seed = self.mnemo.to_seed(seed_phrase)

            path = f"m/44'/501'/{i}'/0'"
            keypair = Keypair.from_seed_and_derivation_path(seed, path)
            public_key = keypair.pubkey()
            private_key = base58.b58encode(keypair.secret() + base58.b58decode(str(keypair.pubkey()))).decode('utf-8')

            self.wallets.append(
                {
                    "seed_phrase": seed_phrase,
                    "address": public_key,
                    "private_key": private_key,
                }
            )
            
    def run_evm(self):
        if self.type_var.get() == "1":
            seed_phrase = self.generate_seed_phrases()
            self.generate_evm_wallets(seed_phrase, self.num_of_wallets_var.get())
        elif self.type_var.get() == "2":
            for i in range(self.num_of_wallets_var.get()):
                seed_phrase = self.generate_seed_phrases()
                self.generate_evm_wallets(seed_phrase, 1)
                
    def run_svm(self):
        if self.type_var.get() == "1":
            seed_phrase = self.generate_seed_phrases()
            self.generate_svm_wallets(seed_phrase, self.num_of_wallets_var.get())
        elif self.type_var.get() == "2":
            for i in range(self.num_of_wallets_var.get()):
                seed_phrase = self.generate_seed_phrases()
                self.generate_svm_wallets(seed_phrase, 1)

    def current_time(self):
        return datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

    def save(self):
        filename = f"wallets_{self.current_time()}.csv"

        for index, item in enumerate(self.wallets):
            item["index"] = index + 1

        with open(filename, mode="w", newline="") as csvfile:
            fieldnames = ["index", "seed_phrase", "address", "private_key"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # Ghi tiêu đề
            writer.writerows(self.wallets)  # Ghi các hàng dữ liệu

        self.wallets = []
        os.startfile(filename)

    # endregion

    # region run
    def validate_number(self):
        try:
            num = int(self.num_of_wallets_var.get())
        except:
            CTkMessagebox(
                title="Error",
                message="Invalid number of wallets!!",
                icon="cancel",
                width=300,
                button_width=40,
                button_height=25,
                cancel_button="cross",
                wraplength=500,
            )
            return False

        return True

    def run(self):
        is_valid = self.validate_number()
        if not is_valid:
            return

        if self.vm_var.get() == "evm":
            self.run_evm()
        elif self.vm_var.get() == "svm":
            self.run_svm()
        
        self.save()

    # endregion


if __name__ == "__main__":
    app = WalletGenerator()
    app.mainloop()
