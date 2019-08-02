from setuptools import setup

setup(
    version="0.0.3",
    name="tracking-plan-kit",
    packages=["tracking_plan", "cli", "segment"],
    include_package_data=True,
    install_requires=["requests", "stacklogging", "click", "pyyaml", "inflection"],
    entry_points={
        "console_scripts": ["tracking-plan=cli.main:cli"]
    }
)