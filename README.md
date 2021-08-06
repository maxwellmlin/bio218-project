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
* You will likely need to create Personal Access Token (PAT) for use during the Installation step. Steps for creating a PAT can be found [here](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) 


Installation
------------

* Clone the repository onto your machine by entering this command in your terminal:
  ```
  $ git clone https://gitlab.com/haaselab/biological_clocks_class.git
  ```
* You will be prompted to enter your Gitlab username and password. Enter your username but for the password use your PAT.
* Change into the `biological_clocks_class` directory, create a conda environment and install packages:
  ```
  $ cd biological_clocks_class
  $ conda env create -f conda_req.yml
  $ ipython kernel install --user --name=BioClocksClass
  ```
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
            <tr><td>Cryptococcus neoformans</td><td>Cell Cycle</td><td>Wild-type</td><td>10 min</td><td>230 min</td><td>Cneoformans_RNAseq</td><td>RNAseq</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/27918582/">27918582</a></td></tr>
            <tr><td>Homo Sapiens</td><td>Cell Cycle</td><td>K562 Wild-type</td><td>2 hr</td><td>48 hr</td><td>Hsapiens_K562</td><td>RNAseq</td><td>nan</td></tr>
            <tr><td>Homo Sapiens</td><td>Cell Cycle</td><td>HeLA Wild-type</td><td>1 hr</td><td>47 hr</td><td>Hsapiens_HeLa</td><td>Microarray</td><td><a href="https://pubmed.ncbi.nlm.nih.gov/12058064/">12058064</a></td></tr>
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
