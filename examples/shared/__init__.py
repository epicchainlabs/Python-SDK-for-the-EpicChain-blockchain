import pathlib
import os
import sys
import subprocess
import threading
import shlex
import time
import json
from typing import Optional
from epicchain.wallet.wallet import Wallet
from epicchain.core import types

shared_dir = pathlib.Path("shared").resolve(strict=True)

user_wallet = Wallet.from_file(f"{shared_dir}/user-wallet.json", passwords=["123"])
coz_wallet = Wallet.from_file(f"{shared_dir}/epicchain-wallet.json", passwords=["123"])
epicchainxpress_config_path = f"{shared_dir}/default.epicchain-express"
epicchainxpress_batch_path = f"{shared_dir}/setup-epicchainxp-for-tests.batch"
coz_token_hash = types.UInt160.from_string("0x41ee5befd936c90f15893261abbd681f20ed0429")
# corresponds to the XEP-11 token in the `/xep11-token/` dir and deployed with the `coz` account
xep11_token_hash = types.UInt160.from_string(
    "0x35de2913c480c19a7667da1cc3b2fe3e4c9de761"
)


class EpicChainExpress:
    """EpicChain express wrapper"""

    def __init__(
        self,
        config_path: Optional[str] = None,
        batch_path: Optional[str] = None,
        executable_path: Optional[str] = None,
        debug: bool = False,
    ):
        # The full qualified path is needed for correctly capturing streaming stdout with Popen without shell=True
        # The assumption is that the tool is installed in the standard location (as per
        # https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools#install-a-global-tool )
        # Unless specified manually
        if sys.platform == "win32":
            self.prog = f"{pathlib.Path().home()}\\.dotnet\\tools\\epicchainxp"
        else:
            self.prog = f"{pathlib.Path().home()}/.dotnet/tools/epicchainxp"

        self.config_path = (
            config_path if config_path is not None else epicchainxpress_config_path
        )
        self.batch_path = batch_path if batch_path is not None else epicchainxpress_batch_path
        self.debug = debug

        self._process = None
        self._ready = False
        self._stop = False

        with open(self.config_path) as f:
            data = json.load(f)
            port = data["consensus-nodes"][0]["rpc-port"]
            address = data["settings"].get("rpc.BindAddress", "127.0.0.1")
            self.rpc_host = f"http://{address}:{port}"

        if executable_path is not None:
            self._verify_executable(executable_path)
            self.prog = executable_path
        else:
            try:
                subprocess.run(
                    [self.prog, "-h"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                )
            except subprocess.SubprocessError:
                raise ValueError(
                    "Cannot automatically epicchain express executable. Please specify the path"
                )

    def _verify_executable(self, full_path: str):
        if not os.path.isfile(full_path) or not os.access(full_path, os.X_OK):
            raise ValueError(f"Invalid executable: {full_path}")

    def initialize_with(self, batch_path: str):
        print("executing private chain batch...", end="")
        cmd = f"{self.prog} batch -r {batch_path}"
        subprocess.run(shlex.split(cmd), check=True, stdout=subprocess.DEVNULL)
        print("done")

    def run(self):
        print("starting private chain...", end="")
        cmd = f"{self.prog} run -i {self.config_path}"

        self._process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=True,
            shell=False,
        )

        def process_stdout(process):
            for output in iter(process.stdout.readline, b""):
                if self._stop is True:
                    break

                if "EpicChain private chain is running" in output:
                    self._ready = True

                if self.debug:
                    print(output, end="")

        thread = threading.Thread(target=process_stdout, args=(self._process,))
        thread.start()

        while not self._ready:
            time.sleep(0.0001)

        print("done")

    def stop(self):
        print("stopping epicchain private chain...", end="")
        # break out of the process_stdout loop
        self._stop = True
        self._process.kill()
        print("done")

    @classmethod
    def at(
        cls,
        executable_path: str,
        config_path: Optional[str] = None,
        batch_path: Optional[str] = None,
        debug: bool = False,
    ):
        return cls(config_path, batch_path, executable_path, debug)

    def __enter__(self):
        if self.batch_path is not None:
            self.initialize_with(self.batch_path)
        self.run()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
