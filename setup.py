from distutils.core import setup
import sys


if len(sys.argv) > 2:
    version = sys.argv[1]
    setup(
        name="zypher_trading_bot",  # How you named your package folder (MyLib)
        packages=["zypher_trading_bot"],  # Chose the same as "name"
        version=version,  # Start with a small number and increase it with every change you make
        license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
        description="Trading Bot",  # Give a short description about your library
        author="Sebastian Oderland",  # Type in your name
        author_email="sebastian.oderland@oderland.se",  # Type in your E-Mail
        url="https://github.com/SebastianOderland/zypher_trading_bot",  # Provide either the link to your github or to your website
        download_url="https://github.com/SebastianOderland/zypher_trading_bot/releases/tag/v_"
        + version
        + ".tar.gz",  # I explain this later on
        keywords=["zypher",],  # Keywords that define your package best
        install_requires=["ib_insync",],
        classifiers=[
            "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            "Intended Audience :: Developers",  # Define that your audience are developers
            "Topic :: Software Development :: Build Tools",
            "License :: OSI Approved :: MIT License",  # Again, pick a license
            "Programming Language :: Python :: 3.8",
        ],
    )
