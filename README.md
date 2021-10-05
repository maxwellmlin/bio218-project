# Biological Clocks class

This repository contains material for the Duke University class Biological Clocks.

Requirements
------------
### Conda
* You will need [Conda](https://conda.io/projects/conda/en/latest/index.html) installed. Conda is a package and environment manager and is included in all versions of [Anaconda](https://www.anaconda.com/products/individual) and [Miniconda](https://docs.conda.io/en/latest/miniconda.html). Installation instructions can be found [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

### MPI
* If you do not have `MPI` installed:
    ```
    For MacOS
    $ brew install openmpi
    $ mpiexec --version
    
    For Ubuntu
    $ sudo apt-get install openmpi-bin
    $ mpiexec --version
    ```

### Git
* [Git](https://www.atlassian.com/git/tutorials/what-is-git) is a version control system and can be installed via conda. In your terminal, enter the command:

  ```
  $ conda install git
  ```
### Gitlab ([www.gitlab.com](https://www.gitlab.com))
* You will also need to create a Gitlab account, which you can do [here](https://gitlab.com/users/sign_up). 
* You will likely need to create a Personal Access Token (PAT) for use during the Installation step. Steps for creating a PAT can be found [here](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html). 


Installation
------------

* Clone the repository onto your machine by entering the following command in your terminal. Note that if you have a Windows machine, this command should be run in a cmd (Command Prompt) terminal instead of the Conda terminal. To open cmd, see [here](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/#:~:text=Press%20Windows%2BR%20to%20open,open%20an%20administrator%20Command%20Prompt).
  ```
  $ git clone https://gitlab.com/haaselab/biological_clocks_class.git
  ```
* You will be prompted to enter your Gitlab username and password. Enter your username but for the password use your PAT.
* Change into the `biological_clocks_class` directory, create a conda environment and install packages. To learn more about the command line and commands such as "cd" (change directory) below, see this [crash course](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Command_line). 
  ```
  $ cd biological_clocks_class
  $ git submodule init
  $ git submodule update
  $ conda env create -f conda_req.yml
  $ conda activate BioClocksClass
  $ ipython kernel install --user --name=BioClocksClass
  ```

Tools
------------
* pyJTK
* pyDL
* DLxJTK
* LEM

Datasets
------------

Below is a table describing the datasets available within this repository. The last column, titled PMID, contains the pubmed ID for the article the dataset is associated with. Clicking the ID will link you to the article on Pubmed.
<br>

<table>
    <thead>
      <tr>
        <th>Organism</th><th>Process</th><th>Condition</th><th>Sampling Frequency</th><th>Sampling Duration</th><th>Dataset</th><th>Type</th><th>PMID</th>
      </tr>
    </thead>
        <tbody>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>Wild-type replicate 1</td><td>16 min</td><td>254 min</td><td>Scerevisiae_WT1_Microarray</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/18463633/">18463633</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>Wild-type replicate 2</td><td>16 min</td><td>262 min</td><td>Scerevisiae_WT2_Microarray</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/18463633/">18463633</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>Wild-type</td><td>5 min</td><td>245 min</td><td>Scerevisiae_RNAseq</td><td>RNAseq</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/27918582/">27918582</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>No APC activity replicate 1</td><td>20 min</td><td>300 min</td><td>Scerevisiae_noAPC_r1</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/25200947/">25200947</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>No APC activity replicate 2</td><td>20 min</td><td>360 min</td><td>Scerevisiae_noAPC_r2</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/25200947/">25200947</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>No cyclin-CDK activity replicate 1</td><td>16 min</td><td>262 min</td><td>Scerevisiae_noCDK_r1</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/18463633/">18463633</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>No cyclin-CDK activity replicate 2</td><td>16 min</td><td>254 min</td><td>Scerevisiae_noCDK_r2</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/18463633/">18463633</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>DNA Damage Checkpoint activated replicate 1</td><td>Uneven min</td><td>260 min</td><td>Scerevisiae_DRC_r1</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/25200947/">25200947</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>DNA Damage Checkpoint activated replicate 2</td><td>Uneven min</td><td>260 min</td><td>Scerevisiae_DRC_r2</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/25200947/">25200947</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>Perturbed DNA Damage Checkpoint activated + no APC activity replicate 1</td><td>18 min</td><td>360 min</td><td>Scerevisiae_xDRC_noAPC_r1</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/25200947/">25200947</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>Perturbed DNA Damage Checkpoint activated + no APC activity replicate 2</td><td>18 min</td><td>360 min</td><td>Scerevisiae_xDRC_noAPC_r2</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/25200947/">25200947</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>Spindle Assembly Checkout activated replicate 1</td><td>15 min</td><td>245 min</td><td>Scerevisiae_SpAC_r1</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/25200947/">25200947</a></td></tr>
            <tr><td>Saccharomyces cerevisiae</td><td>Cell Cycle</td><td>Spindle Assembly Checkout activated replicate 2</td><td>15 min</td><td>245 min</td><td>Scerevisiae_SpAC_r1</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/25200947/">25200947</a></td></tr>
            <tr><td>Cryptococcus neoformans</td><td>Cell Cycle</td><td>Wild-type</td><td>10 min</td><td>230 min</td><td>Cneoformans_RNAseq</td><td>RNAseq</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/27918582/">27918582</a></td></tr>
            <tr><td>Homo Sapiens</td><td>Cell Cycle</td><td>K562 cell line</td><td>2 hr</td><td>48 hr</td><td>Hsapiens_K562</td><td>RNAseq</td><td>nan</td></tr>
            <tr><td>Homo Sapiens</td><td>Cell Cycle</td><td>HeLA cell line</td><td>1 hr</td><td>47 hr</td><td>Hsapiens_HeLa</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/12058064/">12058064</a></td></tr>
            <tr><td>Homo Sapiens</td><td>Cell Cycle</td><td>HeCat cell line</td><td>3 hr</td><td>33 hr</td><td>Hsapiens_HeCat</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/23325852/">23325852</a></td></tr>
            <tr><td>Ophiocordyceps kimflemingiae</td><td>Circadian</td><td>light-dark</td><td>4 hr</td><td>48 hr</td><td>Okimflemingiae_DD_RPKM</td><td>RNAseq</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/29099875/">29099875</a></td></tr>
            <tr><td>Ophiocordyceps kimflemingiae</td><td>Circadian</td><td>dark-dark</td><td>4 hr</td><td>48 hr</td><td>Okimflemingiae_LD_RPKM</td><td>RNAseq</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/29099875/">29099875</a></td></tr>
            <tr><td>Phaeodactylum tricornutum</td><td>Circadian</td><td>light-dark</td><td>Uneven</td><td>27 hr</td><td>Ptricornutum_LD</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/23209127/">23209127</a></td></tr>
            <tr><td>Mus musculus</td><td>Circadian</td><td>dark-dark Liver </td><td>2 hr</td><td>48 hr</td><td>Mmusculus_liver_DDHC</td><td>RNAseq</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/25349387/">25349387</a></td></tr>
            <tr><td>Arabidopsis thaliana</td><td>Circadian</td><td>light-dark</td><td>4 hr</td><td>48 hr</td><td>Athaliana_LD</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/18248097/">18248097</a></td></tr>
            <tr><td>Arabidopsis thaliana</td><td>Circadian</td><td>light-light</td><td>4 hr</td><td>48 hr</td><td>Athaliana_LL</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/18248097/">18248097</a></td></tr>
            <tr><td>Kalanchoe fedtschenkoi</td><td>Circadian</td><td>light-dark</td><td>2 hr</td><td>48 hr</td><td>Kfedtschenkoi_LD</td><td>RNAseq</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/29196618/">29196618</a></td></tr>
            <tr><td>Kalanchoe fedtschenkoi</td><td>Circadian</td><td>light-light</td><td>2 hr</td><td>48 hr</td><td>Kfedtschenkoi_LL</td><td>RNAseq</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/29196618/">29196618</a></td></tr>
            <tr><td>Plasmodium falciparum</td><td>Intraerythrocytic Development Cycle</td><td>in vitro 3D7</td><td>3 hr</td><td>60 hr</td><td>Pfalciparum_3D7</td><td>RNAseq</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/32409472/">32409472</a></td></tr>
            <tr><td>Plasmodium vivax</td><td>Intraerythrocytic Development Cycle</td><td>ex vivo Participant 08</td><td>3 hr</td><td>48 hr</td><td>Pvivax_08</td><td>RNAseq</td><td>nan</td></tr>
            <tr><td>Plasmodium vivax</td><td>Intraerythrocytic Development Cycle</td><td>ex vivo Participant 09</td><td>3 hr</td><td>48 hr</td><td>Pvivax_09</td><td>RNAseq</td><td>nan</td></tr></tbody>
  </table>

Can't or don't want to install on your own machine? Let's use a virtual machine courtesy of Duke University.
----
https://vcm.duke.edu/

Reserve a VM

ubunto 20

agree

wait for email

putty (Windows)

sudo apt-get update

sudo apt-get install curl

curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash Miniconda3-latest-Linux-x86_64.sh
  - yes to all

create access token

clone repo using as password

$ cd biological_clocks_class
$ git submodule init
$ git submodule update
$ conda env create -f conda_req.yml
$ 
$ ipython kernel install --user --name=BioClocksClass

<!-- Troubleshooting -->
<!-- ------------ -->