import os
import requests
from tqdm import tqdm


class Downloader:

    CHUNK_SIZE = 1024 * 1024  # 1 MB

    def __init__(self, timeout=30):
        self.timeout = timeout

    def download(
        self,
        url,
        name,
        directory,
    ):

        os.makedirs(
            directory,
            exist_ok=True,
        )

        destination = os.path.join(
            directory,
            name,
        )

        #
        # Skip existing file
        #

        if os.path.exists(destination):

            print()
            print(
                f"[SKIP] Already exists: "
                f"{destination}"
            )

            return destination

        print()
        print("=" * 60)
        print(f"DOWNLOAD : {name}")
        print(f"URL      : {url}")
        print(f"DEST     : {destination}")
        print("=" * 60)

        try:

            response = requests.get(
                url,
                stream=True,
                timeout=self.timeout,
            )

            response.raise_for_status()

            total_size = int(
                response.headers.get(
                    "content-length",
                    0,
                )
            )

            with open(
                destination,
                "wb",
            ) as file:

                with tqdm(
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=name,
                ) as progress:

                    for chunk in response.iter_content(
                        chunk_size=self.CHUNK_SIZE
                    ):

                        if not chunk:
                            continue

                        file.write(chunk)

                        progress.update(
                            len(chunk)
                        )

            print(
                f"[DONE] {destination}"
            )

            return destination

        except requests.RequestException as e:

            print(
                f"[ERROR] Download failed: {url}"
            )

            print(
                f"        {e}"
            )

            return None

        except OSError as e:

            print(
                f"[ERROR] Could not write: "
                f"{destination}"
            )

            print(
                f"        {e}"
            )

            return None