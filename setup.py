from setuptools import find_packages, setup

setup(
    name='mcqgenerator',                # Name of your package
    version='0.01',                     # Version of the package
    author='Nagesh',                    # Author's name
    author_email='nageshp613@gmail.com',# Author's email
    description='A tool for generating MCQs', # Short description
    #long_description=open('README.md').read(), # Detailed description from README.md (if you have it)
    #long_description_content_type='text/markdown', # Format of long description
    #url='https://github.com/Nageshpermand/MCQ_Generator', # URL for the project
    packages=find_packages(),           # Automatically find and include packages
    install_requires=[                  # List of dependencies
        "numpy",                        # Example dependencies (adjust according to your needs)
        "pandas",
        "scikit-learn","openai","langchain","streamlit","python-dotenv","PyPDF2"],
    )
