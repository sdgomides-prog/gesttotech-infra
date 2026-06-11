from setuptools import setup, find_packages

with open("requirements.txt") as f:
      install_requires = f.read().strip().split("\n")

setup(
      name="kore",
      version="0.1.0",
      description="Kore Pagamento - PIX via HappyPay para Frappe/ERPNext",
      author="GesttoTech",
      author_email="dev@gesttotech.com.br",
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=install_requires,
)
