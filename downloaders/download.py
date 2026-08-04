from pathlib import Path
from tqdm import tqdm
import requests


class Downloader:

    def download(
        self,
        assets: list,
        destination: Path,
        pattern: str | None = None
    ):

        for asset in assets:

            if pattern and not asset["name"].endswith(pattern):
                continue

            file_path = destination / asset["name"]

            if file_path.exists():
                print(f"[SKIP] {asset['name']}")
                continue

            print(f"[DOWNLOAD] {asset['name']}")

            response = requests.get(
                asset["url"],
                stream=True,
                timeout=60
            )

            response.raise_for_status()

            total_size = int(
                response.headers.get("content-length", 0)
            )

            with open(file_path, "wb") as file:

                with tqdm(
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=asset["name"],
                ) as progress:

                    for chunk in response.iter_content(
                        chunk_size=1024 * 1024
                    ):

                        if chunk:

                            file.write(chunk)

                            progress.update(
                                len(chunk)
                            )

            print(f"[DONE] {asset['name']}")

    def download_public_key(
        self,
        url: str,
        key_name: str,
        destination: Path
    ):
        # DOWNLOAD PUBLIC KEY FROM URL #
        try: 
            key_url= f"{url}/{key_name}"
            response = requests.get(
                key_url,
                stream=True,
                timeout=60
            )
            response.raise_for_status()
        except:
            print(f"[FAILED] Could not download public key from {key_url}")
            return

        # SAVE PUBLIC KEY TO DESTINATION #
        with open (destination / key_name, "wb") as file:
            file.write(response.content)