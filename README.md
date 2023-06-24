# MirPredict <img src="lib/assets/icon.gif" alt="Genlingo Logo" width="30">

MirPredict is a small app designed to map micro RNAs to their corresponding RNAs using two of the biggest engines: 'DianaDB' and 'MirDB'. The app utilizes headless Selenium browsers to scrape data from the web and performs subsequent analysis. The search process involves leveraging data from three additional sources: 'Ensembl', 'MirBase', and 'ProteinAtlas'.

<img src="shot_1.jpg" width="500">

## Download & Install

1. Click on the following link to download the setup file.
2. Install the application locally on your PC.

| Version | Link |
|---------|------|
| 0.5     | [mirPredict_v0.5](https://drive.google.com/file/d/19THfX3aZCVVAPc10DKsL8lz4ab0WXYgG/view?usp=sharing) |

## Tissue Expression

The tissue expression data is sourced from the www.proteinatlas.org database and includes four reliability categories: Approved, Enhanced, Supported, and Uncertain. In this app, entries with uncertain reliability are omitted from the query results.

Additionally, the expression levels are categorized from high to not detected, excluding the 'Not Representative' category.

---

### Acknowledgment

This project was conducted in collaboration with laboratory of prof. Heromana Sorek at the Hebrew University. I am grateful for their support and guidance throughout the development process.

Please note that this README is a brief overview of the 'mirPredict' app. For more detailed documentation and usage instructions, refer to the documentation files or comments within the source code.

For any feedback, questions, or issues, please contact me via email at [raz3zeevy@gmail.com](mailto:raz3zeevy@gmail.com).

## License

[MIT License](LICENSE)
